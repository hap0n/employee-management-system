"""add employee id to tasks

Revision ID: 36fc5f129053
Revises: 674653e35be5
Create Date: 2021-12-25 01:09:37.948638

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "36fc5f129053"
down_revision = "674653e35be5"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE tasks
        ADD employee_id INT NOT NULL;
        """
    )
    op.execute(
        """
        ALTER TABLE tasks
        ADD CONSTRAINT fk_employee_id FOREIGN KEY (employee_id) REFERENCES employees(id);
        """
    )


def downgrade():
    pass
