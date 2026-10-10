"""Add arr instances for Custom Format rejection handling

Revision ID: 5d2e7a91c4f0
Revises: c3a1f8e92b47
Create Date: 2026-10-10 19:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d2e7a91c4f0'
down_revision = 'c3a1f8e92b47'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'arr_instance' not in inspector.get_table_names():
        op.create_table(
            'arr_instance',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('name', sa.String(length=100), nullable=False, unique=True),
            sa.Column('arr_type', sa.String(length=20), nullable=False),
            sa.Column('url', sa.String(length=200), nullable=False),
            sa.Column('api_key', sa.String(length=100), nullable=False),
            sa.Column('remove_category_on_cf_not_upgrade', sa.Boolean(), nullable=True),
        )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'arr_instance' in inspector.get_table_names():
        op.drop_table('arr_instance')
