"""add_core_tables

Revision ID: 367f848a6f19
Revises: 7c3e5aca9610
Create Date: 2024-07-26 16:39:09.398046+07:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "367f848a6f19"
down_revision: Union[str, None] = "7c3e5aca9610"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "devices",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("device_id", sa.Uuid(), nullable=False),
        sa.Column("broswer", sa.String(), nullable=False),
        sa.Column("os", sa.String(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id"),
    )
    op.create_table(
        "groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("member_counts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("dob", sa.Date(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("gender", sa.String(), nullable=False),
        sa.Column("backup_email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username")
    )
    op.create_table(
        "crypto_keys",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("enc_pri", sa.String(), nullable=False),
        sa.Column("public_key", sa.String(), nullable=False),
        sa.Column("salt", sa.String(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("site", sa.String(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("enc_credentials", sa.String(), nullable=False),
        sa.Column("added_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "session_infos",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("ip", sa.String(), nullable=False),
        sa.Column(
            "status", sa.Enum("SUCCESS", "FAILED", name="status"), nullable=False
        ),
        sa.Column("user_agent", sa.String(), nullable=False),
        sa.Column("device_fk", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["device_fk"],
            ["devices.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users_in_groups",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("group_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "group_id"),
    )
    op.create_table(
        "item_histories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("ip", sa.String(), nullable=False),
        sa.Column(
            "status", sa.Enum("SUCCESS", "FAILED", name="status"), nullable=False
        ),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "personal_items",
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
        ),
        sa.PrimaryKeyConstraint("item_id"),
    )
    op.create_table(
        "shared_items",
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("enc_pri", sa.String(), nullable=False),
        sa.Column("shared_at", sa.DateTime(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["items.id"],
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("item_id"),
    )
    op.create_table(
        "filling_histories",
        sa.Column("history_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["history_id"],
            ["item_histories.id"],
        ),
        sa.PrimaryKeyConstraint("history_id"),
    )
    op.create_table(
        "sharing_histories",
        sa.Column("history_id", sa.Uuid(), nullable=False),
        sa.Column("provider_id", sa.Uuid(), nullable=False),
        sa.Column("recipient_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["history_id"],
            ["item_histories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("history_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sharing_histories")
    op.drop_table("filling_histories")
    op.drop_table("shared_items")
    op.drop_table("personal_items")
    op.drop_table("item_histories")
    op.drop_table("users_in_groups")
    op.drop_table("session_infos")
    op.drop_table("items")
    op.drop_table("crypto_keys")
    op.drop_table("users")
    op.drop_table("groups")
    op.drop_table("devices")
    # ### end Alembic commands ###
