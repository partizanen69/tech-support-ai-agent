from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select
from src.db.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_related_chunks(
        self, embeddings: list[float]
    ) -> Sequence[KnowledgeChunk]:
        stmt = (
            select(KnowledgeChunk)
            .order_by(KnowledgeChunk.embedding.l2_distance(embeddings))
            .limit(3)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
