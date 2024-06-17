"""Initial migration

Revision ID: 5c93120b26d4
Revises: 
Create Date: 2024-06-17 00:18:11.085213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c93120b26d4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('User', 'Admin', name='user_roles'), nullable=False),
    sa.Column('suspended_account', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_table('artists',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('artist_id')
    )
    op.create_index(op.f('ix_artists_artist_id'), 'artists', ['artist_id'], unique=False)
    op.create_table('events',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('event_type', sa.Enum('Festival', 'Personal Concert', name='event_type'), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_events_event_id'), 'events', ['event_id'], unique=False)
    op.create_table('concert_details',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('accommodation', sa.String(), nullable=True),
    sa.Column('transport', sa.String(), nullable=True),
    sa.Column('ticket_price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('physical_tickets', sa.Integer(), nullable=True),
    sa.Column('electronic_tickets', sa.Integer(), nullable=True),
    sa.Column('electronic_ticket_fee', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('culture_tax', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('festival_details',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('accommodation', sa.String(), nullable=True),
    sa.Column('transport', sa.String(), nullable=True),
    sa.Column('merchandise', sa.String(), nullable=True),
    sa.Column('artist_payment', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('festival_details')
    op.drop_table('concert_details')
    op.drop_index(op.f('ix_events_event_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_artists_artist_id'), table_name='artists')
    op.drop_table('artists')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###