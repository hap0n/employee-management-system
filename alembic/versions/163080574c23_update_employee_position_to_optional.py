"""update employee position to optional

Revision ID: 163080574c23
Revises: 85e9ce0d9b9f
Create Date: 2021-12-24 23:26:49.356543

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "163080574c23"
down_revision = "85e9ce0d9b9f"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE employees
            ALTER COLUMN project_position_id DROP NOT NULL;
        """
    )

    op.execute(
        """
        ALTER TABLE employees
            ALTER COLUMN internal_position_id DROP NOT NULL;
        """
    )


def downgrade():
    pass
