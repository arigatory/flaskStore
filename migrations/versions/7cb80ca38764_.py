"""empty message

Revision ID: 7cb80ca38764
Revises: 1217e4f7f4f9
Create Date: 2020-11-01 08:28:06.625467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cb80ca38764'
down_revision = '1217e4f7f4f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('category')
    op.add_column('meals', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'meals', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'meals', type_='foreignkey')
    op.drop_column('meals', 'category_id')
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='category_pkey')
    )
    op.drop_table('categories')
    # ### end Alembic commands ###
