"""Add InventoryAdjustments table

Revision ID: a3f1c2d4e5b6
Revises: 9c87639e84b4
Create Date: 2026-04-05 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3f1c2d4e5b6'
down_revision = '9c87639e84b4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'InventoryAdjustments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('previous_quantity', sa.Integer(), nullable=False),
        sa.Column('new_quantity', sa.Integer(), nullable=False),
        sa.Column('adjustment', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=False),
        sa.Column('adjusted_by', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['Books.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('InventoryAdjustments')
