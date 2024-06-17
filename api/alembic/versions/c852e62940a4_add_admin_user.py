"""Add Admin user

Revision ID: c852e62940a4
Revises: 5c93120b26d4
Create Date: 2024-06-17 00:18:22.303087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, Enum
from app.utils.security_service import get_password_hash


# revision identifiers, used by Alembic.
revision: str = 'c852e62940a4'
down_revision: Union[str, None] = '5c93120b26d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    user_role_enum = sa.Enum('User', 'Admin', name='user_roles')

    users_table = table('users',
                        column('user_id', Integer),
                        column('username', String),
                        column('email', String),
                        column('password', String),
                        column('role', user_role_enum),
                        column('suspended_account', Boolean))

    admin_password_hashed = get_password_hash("VoodooRules123!")
    op.bulk_insert(users_table,
                   [
                       {'username': 'Admin',
                        'email': 'admin@thevoodoochildband.com',
                        'password': admin_password_hashed,
                        'role': 'Admin',
                        'suspended_account': False}
                   ])


def downgrade():
    op.execute("DELETE FROM users WHERE email = 'admin@thevoodoochildband.com'")
