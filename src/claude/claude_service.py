import logging
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import re

from src.claude.claude_enums import TicketCategory
from src.claude.claude_client import claude_client


class CategoryResult(BaseModel):
    category: TicketCategory


logger = logging.getLogger(__name__)


class ClaudeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def classify_ticket(
        self, ticket_text: str = None, ticket_subject: str = None
    ) -> TicketCategory:
        prompt = f"""
        Ти є експертом з підтримки користувачів і твоя задача визначити категорію питання в тікеті.
        Класифікуй питання в одну з таких категорій, якщо не можеш визначити, то поверни GENERAL:
        <categories>
            <category>{TicketCategory.AUTHENTICATION_AND_ACCESS_MANAGEMENT.value}</category>
            <category>{TicketCategory.BILLING.value}</category>
            <category>{TicketCategory.TROUBLESHOOTING.value}</category>
            <category>{TicketCategory.GENERAL.value}</category>
        </categories>

        Текст тікету: <ticket_text>{ticket_text}</ticket_text>
        Тема тікету: <ticket_subject>{ticket_subject}</ticket_subject>

        Поверни категорію тікету в форматі json {{ "category": "Категорія яку ти визначила" }}. Повертай тільки json, без пояснень.
        """

        result = await claude_client.call_llm(prompt)

        try:
            json_str = extract_first_json_object(result)
            return CategoryResult.model_validate_json(json_str).category
        except Exception as e:
            logger.error(f"Failed to parse/validate JSON: {e}")
            raise


def extract_first_json_object(text: str) -> str:
    # Remove markdown code fences if present
    text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
    # Find the first {...} block
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response")
    return match.group(0)
