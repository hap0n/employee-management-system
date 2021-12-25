"""create leaves, links, phones, tasks

Revision ID: 674653e35be5
Revises: 163080574c23
Create Date: 2021-12-24 23:54:29.928697

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "674653e35be5"
down_revision = "163080574c23"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TYPE TaskPriority AS ENUM ('minor', 'normal', 'major', 'hot');
        CREATE TYPE TaskStatus AS ENUM ('done', 'in progress', 'selected_for_development');
        CREATE TYPE LeaveType AS ENUM ('vacation', 'sick_leave');
        CREATE TYPE PhoneStatus AS ENUM ('active', 'deprecated');
        CREATE TYPE LeaveStatus AS ENUM ('confirmed', 'rejected', 'pending');
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks(
            id serial PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            priority TaskPriority NOT NULL DEFAULT 'normal',
            status TaskStatus NOT NULL DEFAULT 'selected_for_development',
            assignee_id INT NOT NULL,
            FOREIGN KEY (assignee_id) REFERENCES employees(id),
            reporter_id INT NOT NULL,
            FOREIGN KEY (reporter_id) REFERENCES employees(id),
            created_at timestamp
        );
        
        CREATE TABLE IF NOT EXISTS links(
            id serial PRIMARY KEY,
            name VARCHAR(255),
            link VARCHAR(511),
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS leaves(
            id serial PRIMARY KEY,
            leave_type LeaveType NOT NULL DEFAULT 'vacation',
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status LeaveStatus NOT NULL DEFAULT 'pending',
            approved_by INT,
            requested_at TIMESTAMP NOT NULL,
            approved_at TIMESTAMP,
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS phone_numbers(
            id serial PRIMARY KEY,
            phone VARCHAR(255),
            status PhoneStatus NOT NULL DEFAULT 'active',
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        """
    )


def downgrade():
    pass
