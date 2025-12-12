"""create products table

Revision ID: fe786416943a
Revises: 73079331a218
Create Date: 2025-12-12 20:51:31.633072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe786416943a'
down_revision: Union[str, Sequence[str], None] = '73079331a218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('stock', sa.Integer(), server_default='0', nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('products')
