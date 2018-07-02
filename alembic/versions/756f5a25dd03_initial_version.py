"""Initial version

Revision ID: 756f5a25dd03
Revises:
Create Date: 2018-06-30 14:42:57.527960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '756f5a25dd03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.TEXT(), nullable=False),
        sa.Column('activities', sa.JSON(), nullable=False),
        sa.Column('chart_types', sa.JSON(), nullable=False),
        sa.Column('time_unit', sa.TEXT(), nullable=False),
        sa.Column('month', sa.TEXT(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('created', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('activities')
