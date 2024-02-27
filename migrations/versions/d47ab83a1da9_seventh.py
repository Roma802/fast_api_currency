"""Seventh

Revision ID: d47ab83a1da9
Revises: 6c25a137106a
Create Date: 2024-02-25 13:26:32.703174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd47ab83a1da9'
down_revision: Union[str, None] = '6c25a137106a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
