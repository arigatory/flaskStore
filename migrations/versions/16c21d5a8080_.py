"""empty message

Revision ID: 16c21d5a8080
Revises: 2a71bfe960c9
Create Date: 2020-11-07 03:28:24.398130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c21d5a8080'
down_revision = '2a71bfe960c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'sum')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('sum', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
