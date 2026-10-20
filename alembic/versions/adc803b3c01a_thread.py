"""thread

Revision ID: adc803b3c01a
Revises: ae3a637d0201
Create Date: 2026-10-20 14:48:24.024287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adc803b3c01a'
down_revision: Union[str, Sequence[str], None] = 'ae3a637d0201'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
