"""add added the created_at field to SessionModel

Revision ID: 8c1cc1e70b13
Revises: 19ec6dd8c435
Create Date: 2025-10-17 06:23:07.140405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c1cc1e70b13'
down_revision: Union[str, Sequence[str], None] = '19ec6dd8c435'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
