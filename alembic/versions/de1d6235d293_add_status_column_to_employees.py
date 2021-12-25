"""add status column to employees

Revision ID: de1d6235d293
Revises: 57f67a79ac9e
Create Date: 2021-12-24 19:15:43.085615

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "de1d6235d293"
down_revision = "57f67a79ac9e"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE EmployeeStatus AS ENUM ('works', 'blacklist', 'fired')")

    op.execute(
        """
        ALTER TABLE employees
        ADD status EmployeeStatus NOT NULL DEFAULT 'works';
        """
    )


def downgrade():
    pass
