"""empty message

Revision ID: 9bf76bd0fffa
Revises: 8a1457af7b24
Create Date: 2022-01-27 19:17:58.460287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9bf76bd0fffa'
down_revision = '8a1457af7b24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('eligibility', sa.String(length=100), nullable=False))
    op.add_column('jobs', sa.Column('location', sa.String(length=100), nullable=True))
    op.drop_column('jobs', 'eligiblity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('eligiblity', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('jobs', 'location')
    op.drop_column('jobs', 'eligibility')
    # ### end Alembic commands ###