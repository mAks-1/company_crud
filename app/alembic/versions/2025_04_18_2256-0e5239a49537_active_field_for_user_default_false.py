"""active field for user default=False

Revision ID: 0e5239a49537
Revises: af6600337735
Create Date: 2025-04-18 22:56:16.804264

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e5239a49537"
down_revision: Union[str, None] = "af6600337735"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",  # назва таблиці
        "active",  # назва колонки
        server_default=sa.text("false")
    )



def downgrade() -> None:
    op.alter_column(
        "users",  # назва таблиці
        "active",  # назва колонки
        server_default=sa.text("true")
    )

