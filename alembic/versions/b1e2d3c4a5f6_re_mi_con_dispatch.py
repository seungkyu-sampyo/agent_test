"""re_mi_con_dispatch

Revision ID: b1e2d3c4a5f6
Revises: adc803b3c01a
Create Date: 2026-10-20 16:05:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1e2d3c4a5f6"
down_revision: Union[str, Sequence[str], None] = "adc803b3c01a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "re_mi_con_dispatch",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("invoice_no", sa.String(), nullable=False),
        sa.Column("ship_date", sa.String(), nullable=False),
        sa.Column("plant_code", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invoice_no"),
    )


def downgrade() -> None:
    op.drop_table("re_mi_con_dispatch")
