"""second

Revision ID: 90e5b600e8b2
Revises: 2a95ee318dfd
Create Date: 2024-07-11 12:38:46.555754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e5b600e8b2'
down_revision = '2a95ee318dfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('lastname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('firstname',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('phonenumber',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('confirmpassword',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('confirmpassword',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('phonenumber',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('firstname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('lastname',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###
