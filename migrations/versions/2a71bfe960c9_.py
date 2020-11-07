"""empty message

Revision ID: 2a71bfe960c9
Revises: 7023e25da4bc
Create Date: 2020-11-07 03:04:09.277367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a71bfe960c9'
down_revision = '7023e25da4bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders_meals',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], )
    )
    op.drop_column('orders', 'meals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('meals', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('orders_meals')
    # ### end Alembic commands ###
