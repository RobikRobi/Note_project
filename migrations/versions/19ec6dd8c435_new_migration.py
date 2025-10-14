"""new migration

Revision ID: 19ec6dd8c435
Revises: b584955c5b1c
Create Date: 2025-10-13 10:23:09.401063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19ec6dd8c435'
down_revision: Union[str, Sequence[str], None] = 'b584955c5b1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
