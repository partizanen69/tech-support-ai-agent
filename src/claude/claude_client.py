from src.config.config import settings
import anthropic
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("ClaudeClient")


class ClaudeClient:
    api_url: str = "https://api.anthropic.com/v1/messages"
    api_key: str = settings.CLAUDE_API_KEY
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 2024
    client: anthropic.AsyncAnthropic

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)

    def get_system_prompt(self) -> str:
        return """
        Надавай відповіді на питання українською мовою.
        """

    async def call_llm(self, prompt: str) -> str:
        message = await self.client.messages.create(
            temperature=0,
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.get_system_prompt(),
            messages=[{"role": "user", "content": prompt}],
        )

        logger.info(f"Claude response: {message.content[0].text}")

        return message.content[0].text


claude_client = ClaudeClient()
