"""Add option to skip noHL tagging for downloads awaiting arr import

Revision ID: 9b4e6c2d1a7f
Revises: 5d2e7a91c4f0
Create Date: 2026-10-23 11:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4e6c2d1a7f'
down_revision = '5d2e7a91c4f0'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'instance' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('instance')]
        if 'nohl_skip_arr_import_blocked' not in existing_columns:
            with op.batch_alter_table('instance', schema=None) as batch_op:
                batch_op.add_column(sa.Column('nohl_skip_arr_import_blocked', sa.Boolean(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'instance' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('instance')]
        if 'nohl_skip_arr_import_blocked' in existing_columns:
            with op.batch_alter_table('instance', schema=None) as batch_op:
                batch_op.drop_column('nohl_skip_arr_import_blocked')
