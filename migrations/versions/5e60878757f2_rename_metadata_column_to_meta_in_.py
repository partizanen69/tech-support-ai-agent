"""rename metadata column to meta in knowledge_chunks

Revision ID: 5e60878757f2
Revises: 5d578a54ab47
Create Date: 2025-06-29 11:55:32.039165

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e60878757f2"
down_revision: Union[str, Sequence[str], None] = "5d578a54ab47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("knowledge_chunks", "metadata", new_column_name="meta")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("knowledge_chunks", "meta", new_column_name="metadata")
