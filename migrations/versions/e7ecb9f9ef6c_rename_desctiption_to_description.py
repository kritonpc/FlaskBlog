"""rename desctiption  to description

Revision ID: e7ecb9f9ef6c
Revises: 7d329d32a9da
Create Date: 2022-01-02 18:06:57.945069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ecb9f9ef6c'
down_revision = '7d329d32a9da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=256), nullable=True))
        batch_op.drop_column('desctiption')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('desctiption', sa.VARCHAR(length=256), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###
