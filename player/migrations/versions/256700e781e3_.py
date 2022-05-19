"""empty message

Revision ID: 256700e781e3
Revises: 
Create Date: 2022-03-24 15:12:24.777606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256700e781e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('query',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('user_in', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('songs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=1000), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('some_bs', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('songs')
    op.drop_table('query')
    # ### end Alembic commands ###
