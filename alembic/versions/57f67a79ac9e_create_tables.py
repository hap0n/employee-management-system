"""create tables

Revision ID: 57f67a79ac9e
Revises: 
Create Date: 2021-12-24 08:47:26.813136

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "57f67a79ac9e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS documents(
            id serial PRIMARY KEY,
            s3_bucket VARCHAR(255) UNIQUE NOT NULL
        );
        
        CREATE TYPE DivisionStatus AS ENUM ('in progress', 'completed', 'gathering', 'cancelled');
        CREATE TYPE TeamStatus AS ENUM ('active', 'deprecated', 'gathering');
        CREATE TYPE PositionStatus AS ENUM ('active', 'deprecated');
        
        CREATE TABLE IF NOT EXISTS positions(
            id serial PRIMARY KEY,
            status PositionStatus NOT NULL DEFAULT 'active',
            name VARCHAR(255) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS internal_positions(
            id serial PRIMARY KEY,
            position_id INT NOT NULL,
            FOREIGN KEY (position_id) REFERENCES positions(id),
            reports_to INT,
            FOREIGN KEY (reports_to) REFERENCES internal_positions(id)
        );
        
        CREATE TABLE IF NOT EXISTS project_positions(
            id serial PRIMARY KEY,
            position_id INT NOT NULL,
            FOREIGN KEY (position_id) REFERENCES positions(id),
            reports_to INT,
            FOREIGN KEY (reports_to) REFERENCES project_positions(id)
        );
        
        CREATE TABLE IF NOT EXISTS employees(
            id serial PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            middle_name VARCHAR(255),
            last_name VARCHAR(255) NOT NULL,
            info TEXT,
            date_of_birth DATE,
            project_position_id INT NOT NULL,
            FOREIGN KEY (project_position_id) REFERENCES project_positions(id),
            internal_position_id INT NOT NULL,
            FOREIGN KEY (internal_position_id) REFERENCES internal_positions(id),
            hired_on DATE NOT NULL,
            fired_on DATE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS company_info(
            name VARCHAR(255) NOT NULL,
            description TEXT,
            lead_id INT,
            FOREIGN KEY (lead_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS company_docs(
            document_id INT UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS divisions(
            id serial PRIMARY KEY,
            status DivisionStatus NOT NULL DEFAULT 'gathering',
            name VARCHAR(255) NOT NULL,
            lead_id INT,
            FOREIGN KEY (lead_id) REFERENCES employees(id)
        );
        
        CREATE TABLE IF NOT EXISTS teams(
            id serial PRIMARY KEY,
            status TeamStatus NOT NULL DEFAULT 'gathering',
            name VARCHAR(255) NOT NULL,
            lead_id INT,
            FOREIGN KEY (lead_id) REFERENCES employees(id),
            division_id INT,
            FOREIGN KEY (division_id) REFERENCES divisions(id)
        );
        
        CREATE TABLE IF NOT EXISTS holidays(
            id serial PRIMARY KEY,
            date DATE NOT NULL,
            name VARCHAR(255) NOT NULL
        );
        
        
        
        --
        CREATE TABLE IF NOT EXISTS employee_team_xrfs(
            id serial PRIMARY KEY,
            employee_id INT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            team_id INT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams(id)
        );
        
        CREATE TABLE IF NOT EXISTS doc_team_xrfs(
            id serial PRIMARY KEY,
            document_id INT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            team_id INT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams(id)
        );
        
        CREATE TABLE IF NOT EXISTS doc_division_xrfs(
            id serial PRIMARY KEY,
            document_id INT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            division_id INT NOT NULL,
            FOREIGN KEY (division_id) REFERENCES divisions(id)
        );

        """
    )


def downgrade():
    pass
