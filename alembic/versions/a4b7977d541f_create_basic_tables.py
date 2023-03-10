"""create basic tables

Revision ID: a4b7977d541f
Revises: 
Create Date: 2022-07-19 10:01:41.883790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "a4b7977d541f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    role_table = op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "name",
            sa.Enum("user", "moderator", "admin", name="roleenum"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    role_data = [
        {"id": 1, "name": "user"},
        {"id": 2, "name": "moderator"},
        {"id": 3, "name": "admin"},
    ]
    op.bulk_insert(role_table, role_data)

    user_table = op.create_table(
        "domain_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nick", sa.String(), nullable=False, unique=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("user_role_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_role_id"],
            ["role.id"],
        ),
        sa.UniqueConstraint("nick"),
        sa.UniqueConstraint("email"),
    )
    user_data = [
        {
            "id": "0000000000000000000",
            "nick": "super_admin",
            "email": "super@admin.pymeme.eu",
            "user_role_id": 3,
        },
        {
            "id": "0000000000000000001",
            "nick": "mod",
            "email": "mod@admin.pymeme.eu",
            "user_role_id": 2,
        },
    ]
    op.bulk_insert(user_table, user_data)

    status_table = op.create_table(
        "status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "name",
            sa.Enum("approved", "unapproved", name="memestatusenum"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    status_data = [
        {"id": 1, "name": "unapproved"},
        {"id": 2, "name": "approved"},
    ]
    op.bulk_insert(status_table, status_data)

    op.create_table(
        "meme",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid ()")
        ),
        sa.Column("name", sa.String(), nullable=True, unique=False),
        sa.Column("like", sa.Integer(), nullable=False, unique=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("date_add", sa.DateTime(), nullable=False, unique=False, server_default=sa.text("now()")),
        sa.Column("date_mod", sa.DateTime(), nullable=True, unique=False),
        sa.Column("nick", sa.String(), nullable=False, unique=False),
        sa.Column("description", sa.String(), nullable=True, unique=False),
        sa.Column("best", sa.Boolean(), nullable=False, unique=False, default=False),
        sa.Column("alias", sa.String(), nullable=False, unique=True, default=False),
        sa.Column("width", sa.Integer(), nullable=False, unique=False, default=False),
        sa.Column("height", sa.Integer(), nullable=False, unique=False, default=False),
        sa.Column("accepted_by_user", sa.String(), nullable=True, unique=False, default=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["status.id"],
        ),
    )


def downgrade() -> None:
    pass
