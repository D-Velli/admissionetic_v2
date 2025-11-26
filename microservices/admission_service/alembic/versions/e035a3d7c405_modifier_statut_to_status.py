"""modifier statut to status

Revision ID: e035a3d7c405
Revises: c7eec0cb03dc
Create Date: 2025-11-26 06:00:33.836906
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e035a3d7c405"
down_revision: Union[str, Sequence[str], None] = "c7eec0cb03dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "admissions",
        "statut",  # ancien nom
        new_column_name="status",
        existing_type=sa.Enum(
            "EN_ATTENTE",
            "ACCEPTEE",
            "REFUSEE",
            "ANNULEE",
            name="statut_admission_enum",
        ),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "admissions",
        "status",  # nouveau nom
        new_column_name="statut",
        existing_type=sa.Enum(
            "EN_ATTENTE",
            "ACCEPTEE",
            "REFUSEE",
            "ANNULEE",
            name="statut_admission_enum",
        ),
        existing_nullable=False,
    )
