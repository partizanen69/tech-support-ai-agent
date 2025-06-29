import os
import glob
import asyncio
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.db import AsyncSessionLocal
from src.db.knowledge_chunk import KnowledgeChunk
from tqdm import tqdm

EMBED_DIM = 384  # all-MiniLM-L6-v2
CHUNK_SIZE = 500  # chars per chunk
BATCH_SIZE = 16
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

KB_PATH = os.path.join(os.path.dirname(__file__), "../../docs/knowledge-base/*.md")


def chunk_markdown(text, chunk_size=CHUNK_SIZE):
    # Simple paragraph-based chunking
    paras = text.split("\n\n")
    chunks = []
    buf = ""
    for para in paras:
        if len(buf) + len(para) < chunk_size:
            buf += para + "\n\n"
        else:
            if buf:
                chunks.append(buf.strip())
            buf = para + "\n\n"
    if buf:
        chunks.append(buf.strip())
    return chunks


async def embed_and_insert_batch(
    session: AsyncSession, source_file: str, chunks: list[str], model
):
    embeddings = model.encode(
        chunks,
        show_progress_bar=False,
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
    )

    for chunk, embedding in zip(chunks, embeddings):
        kc = KnowledgeChunk(
            source_file=source_file,
            chunk_text=chunk,
            embedding=embedding.tolist(),
            meta=None,
        )
        session.add(kc)


async def main():
    model = SentenceTransformer(MODEL_NAME)
    files = glob.glob(KB_PATH)
    async with AsyncSessionLocal() as session:
        for file in tqdm(files, desc="Files"):
            with open(file, encoding="utf-8") as f:
                text = f.read()
            chunks = chunk_markdown(text)
            # Batch for efficiency
            for i in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[i : i + BATCH_SIZE]
                await embed_and_insert_batch(
                    session, os.path.basename(file), batch, model
                )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
