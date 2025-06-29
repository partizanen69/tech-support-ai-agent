from sqlalchemy.ext.asyncio import AsyncSession
from src.db.knowledge_chunk import KnowledgeChunk
from src.knowledge.knowledge_repository import KnowledgeRepository
from src.embeddings.embeddings_service import embeddings_service
from dataclasses import dataclass
from typing import Optional


@dataclass
class KnowledgeChunkDTO:
    id: int
    source_file: str
    chunk_text: str
    embedding: list[float]
    meta: Optional[dict] = None


class KnowledgeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.knowledge_repository = KnowledgeRepository(db)

    async def get_related_chunks(
        self, ticket_text: str, ticket_subject: str
    ) -> list[KnowledgeChunkDTO]:
        embeddings = embeddings_service.get_embedding(f"{ticket_text} {ticket_subject}")
        chunks = await self.knowledge_repository.get_related_chunks(embeddings)

        return [self.knowledge_chunk_to_dto(chunk) for chunk in chunks]

    def knowledge_chunk_to_dto(self, chunk: KnowledgeChunk) -> KnowledgeChunkDTO:
        return KnowledgeChunkDTO(
            id=chunk.id,
            source_file=chunk.source_file,
            chunk_text=chunk.chunk_text,
            embedding=chunk.embedding,
            meta=chunk.meta,
        )
