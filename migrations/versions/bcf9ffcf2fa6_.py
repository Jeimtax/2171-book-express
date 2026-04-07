"""Baseline migration

Revision ID: bcf9ffcf2fa6
Revises: 
Create Date: 2026-04-03 13:08:44.910806

"""
# revision identifiers, used by Alembic.
revision = 'bcf9ffcf2fa6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Baseline revision for an existing schema. Keep this empty so
    # fresh databases can proceed to later table-creation migrations.
    pass


def downgrade():
    pass
