"""add_role_column_back

Revision ID: 045568c610e5
Revises: 730d4c8af340
Create Date: 2025-12-13 06:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '045568c610e5'
down_revision: Union[str, Sequence[str], None] = '730d4c8af340'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(length=20), server_default='user', nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'role')
