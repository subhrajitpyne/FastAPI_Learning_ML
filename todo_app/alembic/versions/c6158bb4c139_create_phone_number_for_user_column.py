"""Create Phone Number for user column

Revision ID: c6158bb4c139 ***Revision ID***
Revises: 
Create Date: 2025-06-02 17:11:41.326084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6158bb4c139'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number',sa.String(50),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
