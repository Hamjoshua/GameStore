"""Изменение в Game под грядущие нерелизнутые игры

Revision ID: b384873b8146
Revises: 6a53b9c60555
Create Date: 2021-09-16 10:40:41.667289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b384873b8146'
down_revision = '6a53b9c60555'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('game', sa.Column('price', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('game', 'price')
