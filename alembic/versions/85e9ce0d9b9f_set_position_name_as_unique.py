"""set position name as unique

Revision ID: 85e9ce0d9b9f
Revises: de1d6235d293
Create Date: 2021-12-24 21:19:15.320006

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "85e9ce0d9b9f"
down_revision = "de1d6235d293"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE positions
        ADD UNIQUE (name);
        """
    )


def downgrade():
    pass
