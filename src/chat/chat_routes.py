from fastapi import APIRouter
from src.claude.claude_service import ClaudeService, TicketCategory
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
    category = await claude_service.classify_ticket(
        ticket_text=request.description, ticket_subject=request.description
    )

    logger.info(f"Ticket category: {category}")

    return ChatResponse(
        answer=f"Received your question about '{request.subject}'. We'll get back to you at {request.user_email}."
    )
