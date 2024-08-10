"""alter user table

Revision ID: 626fec98b18f
Revises: 367f848a6f19
Create Date: 2024-08-10 20:05:28.154515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '626fec98b18f'
down_revision: Union[str, None] = '367f848a6f19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('devices', sa.Column('browser', sa.String(), nullable=False))
    op.drop_column('devices', 'broswer')
    op.add_column('session_infos', sa.Column('type', sa.Enum('NEW', 'ACTIVE', 'LEAVE', name='sessiontype'), nullable=False))
    op.add_column('session_infos', sa.Column('token', sa.String(), nullable=False))
    op.drop_column('session_infos', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session_infos', sa.Column('status', postgresql.ENUM('SUCCESS', 'FAILED', name='status'), autoincrement=False, nullable=False))
    op.drop_column('session_infos', 'token')
    op.drop_column('session_infos', 'type')
    op.add_column('devices', sa.Column('broswer', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('devices', 'browser')
    # ### end Alembic commands ###
