"""add knowledge_chunks table for vector search

Revision ID: 5d578a54ab47
Revises:
Create Date: 2025-06-28 16:46:18.562001

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "5d578a54ab47"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("source_file", sa.Text, nullable=False),
        sa.Column("chunk_text", sa.Text, nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column("metadata", sa.dialects.postgresql.JSONB, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("knowledge_chunks")
    op.execute("DROP EXTENSION IF EXISTS vector;")
