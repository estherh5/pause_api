"""Index activities external IDs.

Revision ID: ff9e54721e22
Revises: 756f5a25dd03
Create Date: 2026-06-14
"""

from alembic import op

revision = "ff9e54721e22"
down_revision = "756f5a25dd03"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_activities_external_id",
        "activities",
        ["external_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_activities_external_id", table_name="activities")
