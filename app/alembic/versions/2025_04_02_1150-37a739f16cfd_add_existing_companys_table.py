"""add existing companys table

Revision ID: 37a739f16cfd
Revises:
Create Date: 2025-04-02 11:50:58.894046

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37a739f16cfd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Table companys already exists in DB
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
