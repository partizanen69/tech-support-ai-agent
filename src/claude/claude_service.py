import logging
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import re

from src.knowledge.knowledge_service import KnowledgeChunkDTO
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
        <cats>
            <cat>{TicketCategory.AUTHENTICATION_AND_ACCESS_MANAGEMENT.value}</cat>
            <cat>{TicketCategory.BILLING.value}</cat>
            <cat>{TicketCategory.TROUBLESHOOTING.value}</cat>
            <cat>{TicketCategory.GENERAL.value}</cat>
        </cats>

        Текст тікету: <ticket_text>{ticket_text}</ticket_text>
        Тема тікету: <ticket_subject>{ticket_subject}</ticket_subject>

        Поверни категорію тікету в форматі json {{ "category": "Категорія яку ти визначила" }}. Повертай тільки json, без пояснень.
        """

        result = await claude_client.call_llm(prompt)

        try:
            json_str = self.extract_first_json_object(result)
            return CategoryResult.model_validate_json(json_str).category.value
        except Exception as e:
            logger.error(f"Failed to parse/validate JSON: {e}")
            raise

    def extract_first_json_object(self, text: str) -> str:
        # Remove markdown code fences if present
        text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
        # Find the first {...} block
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response")
        return match.group(0)

    async def answer_the_ticket(
        self,
        ticket_text: str = None,
        ticket_subject: str = None,
        related_chunks: list[KnowledgeChunkDTO] = None,
    ) -> str:
        context = "\n\n".join(
            [
                f"<knowledge_chunk>[Джерело: {chunk.source_file}] {chunk.chunk_text}</knowledge_chunk>"
                for chunk in related_chunks
            ]
        )
        prompt = f"""
        Ти є експертом з підтримки користувачів. Використай надані фрагменти знань для відповіді на питання користувача. Якщо відповідь не міститься у фрагментах, дай найкращу відповідь на основі власних знань.

        Фрагменти знань:
        <knowledge_chunks>
        {context}
        </knowledge_chunks>
        
        Текст тікету: <ticket_text>{ticket_text}</ticket_text>
        Тема тікету: <ticket_subject>{ticket_subject}</ticket_subject>

        Дай розгорнуту, корисну відповідь українською мовою. Якщо можливо, посилайся на відповідні фрагменти знань.
        """
        result = await claude_client.call_llm(prompt)
        return result
