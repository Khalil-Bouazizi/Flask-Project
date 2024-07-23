"""empty message

Revision ID: d02d4f84eab1
Revises: 0cfbe7c83018
Create Date: 2024-07-22 17:44:06.787093

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd02d4f84eab1'
down_revision = '0cfbe7c83018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('lastname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('firstname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=1200), autoincrement=False, nullable=False),
    sa.Column('phonenumber', sa.VARCHAR(length=1000), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=15000), autoincrement=False, nullable=False),
    sa.Column('confirmpassword', sa.VARCHAR(length=15000), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('last_connection', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('phonenumber', name='user_phonenumber_key')
    )
    # ### end Alembic commands ###
