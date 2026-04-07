"""Add status to Orders table

Revision ID: d4e5f6a7b8c9
Revises: c2d3e4f5a6b7
Create Date: 2026-04-06 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e5f6a7b8c9'
down_revision = 'c2d3e4f5a6b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'Orders',
        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            server_default='pending'
        )
    )


def downgrade():
    op.drop_column('Orders', 'status')
