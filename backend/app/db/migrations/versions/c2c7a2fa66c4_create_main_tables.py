"""create_cleanings_table

Revision ID: c2c7a2fa66c4
Revises: 1cc5dd49d51c
Create Date: 2021-04-27 00:56:41.387616

"""
from typing import Tuple
from sqlalchemy.dialects.postgresql import UUID
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'c2c7a2fa66c4'
down_revision = '1cc5dd49d51c'
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("username", sa.String(140), unique=True,
                  nullable=False, index=True),
        sa.Column("email", sa.String(140), unique=True,
                  nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean,
                  nullable=False, server_default="False"),
        sa.Column("salt", sa.String(72), nullable=False),
        sa.Column("password", sa.String(144), nullable=False),
        sa.Column("is_active", sa.Boolean(),
                  nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(),
                  nullable=False, server_default="False"),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_profiles_table() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("full_name", sa.String(140), nullable=True),
        sa.Column("phone_number", sa.String(20), nullable=True),
        sa.Column("bio", sa.Text, nullable=True, server_default=""),
        sa.Column("image", sa.String(254), nullable=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey(
            "users.id", ondelete="CASCADE")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(140), nullable=False, index=True),
        sa.Column("description", sa.String(254), nullable=True),
        sa.Column("cleaning_type", sa.String(20), nullable=False,
                  server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("owner", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE")),
        *timestamps(indexed=True),
    )
    op.execute(
        """
        CREATE TRIGGER update_cleanings_modtime
            BEFORE UPDATE
            ON cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_offers_table() -> None:
    op.create_table(
        "user_offers_for_cleanings",
        sa.Column(
            "user_id",  # 'user' is a reserved word in postgres, so going with user_id instead
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "cleaning_id",  # going with `cleaning_id` for consistency
            UUID(as_uuid=True),
            sa.ForeignKey("cleanings.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending", index=True),
        *timestamps(),
    )
    op.create_primary_key("pk_user_offers_for_cleanings", "user_offers_for_cleanings", ["user_id", "cleaning_id"])
    op.execute(
        """
        CREATE TRIGGER update_user_offers_for_cleanings_modtime
            BEFORE UPDATE
            ON user_offers_for_cleanings
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_profiles_table()
    create_cleanings_table()
    create_offers_table()


def downgrade() -> None:
    op.drop_table("user_offers_for_cleanings")
    op.drop_table("cleanings")
    op.drop_table("profiles")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
