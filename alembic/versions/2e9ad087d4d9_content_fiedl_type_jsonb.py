"""content fiedl type jsonb

Revision ID: 2e9ad087d4d9
Revises: b3361595b7a7
Create Date: 2024-09-09 23:21:37.599664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2e9ad087d4d9'
down_revision: Union[str, None] = 'b3361595b7a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'content',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'content',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=False)
    # ### end Alembic commands ###
