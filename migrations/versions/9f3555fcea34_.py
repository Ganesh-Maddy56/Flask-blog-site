"""empty message

Revision ID: 9f3555fcea34
Revises: 
Create Date: 2022-01-31 13:28:47.426043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3555fcea34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CodingProblems',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topic', sa.String(length=100), nullable=False),
    sa.Column('question', sa.String(length=1000), nullable=False),
    sa.Column('expl_input', sa.Text(), nullable=False),
    sa.Column('expl_output', sa.Text(), nullable=False),
    sa.Column('solution', sa.Text(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CodingProblems')
    # ### end Alembic commands ###