"""create_extension_uuid

Revision ID: 1cc5dd49d51c
Revises: 
Create Date: 2021-04-27 00:46:14.693316

"""
from alembic import op
from sqlalchemy.orm import sessionmaker


Session = sessionmaker()


# revision identifiers, used by Alembic
revision = '1cc5dd49d51c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # bind = op.get_bind()
    # session = Session(bind=bind)
    # session.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.execute(
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """
    )


def downgrade() -> None:
    # bind = op.get_bind()
    # session = Session(bind=bind)
    # session.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")
    op.execute(
        """
        DROP EXTENSION IF EXISTS "uuid-ossp";
        """
    )
