"""Add Supplier and Order tables

Revision ID: c1d2e3f4a5b6
Revises: a3f1c2d4e5b6
Create Date: 2026-04-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d2e3f4a5b6'
down_revision = 'a3f1c2d4e5b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=30), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'Orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('items', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['supplier_id'], ['Suppliers.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Orders')
    op.drop_table('Suppliers')
