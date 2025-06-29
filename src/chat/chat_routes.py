from fastapi import APIRouter
from src.knowledge.knowledge_service import KnowledgeService
from src.claude.claude_service import ClaudeService
from src.chat.chat_schemas import ChatRequest, ChatResponse
from src.db.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import logging

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_session)):
    claude_service = ClaudeService(db)
    knowledge_service = KnowledgeService(db)

    category = await claude_service.classify_ticket(
        ticket_text=request.description, ticket_subject=request.description
    )

    logger.info(f"Ticket category: {category}")

    related_chunks = await knowledge_service.get_related_chunks(
        ticket_text=request.description, ticket_subject=request.subject
    )

    answer = await claude_service.answer_the_ticket(
        ticket_text=request.description,
        ticket_subject=request.subject,
        related_chunks=related_chunks,
    )

    return ChatResponse(answer=answer)
