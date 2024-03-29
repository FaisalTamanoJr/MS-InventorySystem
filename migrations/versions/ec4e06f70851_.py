"""empty message

Revision ID: ec4e06f70851
Revises: 10cb37d5d071
Create Date: 2024-03-26 15:03:43.941175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4e06f70851'
down_revision = '10cb37d5d071'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gcash_ref_no', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('gcash_ref_no')

    # ### end Alembic commands ###
