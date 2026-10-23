"""Add rule priority and stop-processing flag

Revision ID: e1c7a4b9d2f3
Revises: 9b4e6c2d1a7f
Create Date: 2026-10-23 15:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1c7a4b9d2f3'
down_revision = '9b4e6c2d1a7f'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'rule' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('rule')]
        with op.batch_alter_table('rule', schema=None) as batch_op:
            if 'priority' not in existing_columns:
                batch_op.add_column(sa.Column('priority', sa.Integer(), nullable=True))
            if 'stop_processing' not in existing_columns:
                batch_op.add_column(sa.Column('stop_processing', sa.Boolean(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'rule' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('rule')]
        with op.batch_alter_table('rule', schema=None) as batch_op:
            if 'stop_processing' in existing_columns:
                batch_op.drop_column('stop_processing')
            if 'priority' in existing_columns:
                batch_op.drop_column('priority')
