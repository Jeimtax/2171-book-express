"""Add split book fields to Order table

Revision ID: c2d3e4f5a6b7
Revises: c1d2e3f4a5b6
Create Date: 2026-04-06 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d3e4f5a6b7'
down_revision = 'c1d2e3f4a5b6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Orders', sa.Column('book_id', sa.Integer(), nullable=True))
    op.add_column('Orders', sa.Column('title', sa.String(length=120), nullable=False, server_default=''))
    op.add_column('Orders', sa.Column('author', sa.String(length=120), nullable=False, server_default=''))
    op.add_column('Orders', sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'))
    op.create_foreign_key('fk_orders_book_id_books', 'Orders', 'Books', ['book_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_orders_book_id_books', 'Orders', type_='foreignkey')
    op.drop_column('Orders', 'quantity')
    op.drop_column('Orders', 'author')
    op.drop_column('Orders', 'title')
    op.drop_column('Orders', 'book_id')
