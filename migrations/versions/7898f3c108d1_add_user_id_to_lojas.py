"""add user_id to lojas

Revision ID: 7898f3c108d1
Revises: 
Create Date: 2025-04-03 23:19:40.621989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7898f3c108d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lojas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_lojas_user_id', 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lojas', schema=None) as batch_op:
        batch_op.drop_constraint('fk_lojas_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
