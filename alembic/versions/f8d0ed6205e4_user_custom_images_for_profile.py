"""user custom images for profile

Revision ID: f8d0ed6205e4
Revises: ae6273f6904a
Create Date: 2021-09-19 14:08:34.968293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8d0ed6205e4'
down_revision = 'ae6273f6904a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_game',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('avatar_url', sa.String(), nullable=True, default='\static\missing_avatar.png'))
    op.add_column('user', sa.Column('bg_url', sa.String(), nullable=True))
    op.add_column('user', sa.Column('body_bg_url', sa.String(), nullable=True))
    # op.drop_column('user', 'url_img')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('url_img', sa.VARCHAR(), nullable=True))
    op.drop_column('user', 'body_bg_url')
    op.drop_column('user', 'bg_url')
    op.drop_column('user', 'avatar_url')
    op.drop_table('user_game')
    # ### end Alembic commands ###
