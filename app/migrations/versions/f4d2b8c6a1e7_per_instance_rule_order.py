"""Per-instance rule order (instance_rules.position)

Revision ID: f4d2b8c6a1e7
Revises: e1c7a4b9d2f3
Create Date: 2026-10-23 15:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4d2b8c6a1e7'
down_revision = 'e1c7a4b9d2f3'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if 'instance_rules' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('instance_rules')]
        if 'position' not in existing_columns:
            with op.batch_alter_table('instance_rules', schema=None) as batch_op:
                batch_op.add_column(sa.Column('position', sa.Integer(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    if 'instance_rules' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('instance_rules')]
        if 'position' in existing_columns:
            with op.batch_alter_table('instance_rules', schema=None) as batch_op:
                batch_op.drop_column('position')
