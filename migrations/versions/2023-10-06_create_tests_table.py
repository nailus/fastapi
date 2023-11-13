"""Create tests table.

Revision ID: ead578c0cc10
Revises: 
Create Date: 2023-10-06 14:32:24.489993

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ead578c0cc10"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("tests",
    sa.Column("id", sa.BigInteger(), nullable=False),
    sa.Column("name", sa.String(), nullable=False),
    sa.Column("created_at", sa.DateTime(), nullable=False),
    sa.Column("updated_at", sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tests_id"), "tests", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tests_id"), table_name="tests")
    op.drop_table("tests")
    # ### end Alembic commands ###