"""create_cleanings_table

Revision ID: c2c7a2fa66c4
Revises: 1cc5dd49d51c
Create Date: 2021-04-27 00:56:41.387616

"""
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic
revision = 'c2c7a2fa66c4'
down_revision = '1cc5dd49d51c'
branch_labels = None
depends_on = None


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        # sa.Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4),
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False,
                  server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )



def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    op.drop_table("cleanings")
