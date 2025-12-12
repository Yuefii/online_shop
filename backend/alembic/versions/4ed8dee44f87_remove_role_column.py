"""remove role column

Revision ID: 4ed8dee44f87
Revises: 9e39dd3b8793
Create Date: 2025-12-12 17:27:42.091467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ed8dee44f87'
down_revision: Union[str, Sequence[str], None] = '9e39dd3b8793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'role')


def downgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(length=20), server_default='staff', nullable=False))
