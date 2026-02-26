"""add_payment_fk_to_bookings

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-01 00:00:00
"""

from alembic import op

revision      = '0004'
down_revision = '0003'
branch_labels = None
depends_on    = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_bookings_payment_id',   # constraint name
        'bookings',                  # from table
        'payments',                  # to table
        ['payment_id'],              # from column
        ['id']                       # to column
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_bookings_payment_id',
        'bookings',
        type_='foreignkey'
    )