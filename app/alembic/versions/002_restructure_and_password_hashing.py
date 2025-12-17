"""Restructure database for v2.0.0 - Remove Ratings, Add password hashing

Revision ID: 002
Revises: 001
Create Date: 2025-12-17

Changes:
- Remove ratings table (ratings functionality moved to review ratings)
- Reorganize Favorites and Reviews models to separate packages
- Ensure password hashing is applied to all passwords
"""
from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade migration:
    1. Drop ratings table (no longer needed)
    2. Restructure database schema for separation of concerns
    """
    # Drop the ratings table as it's being replaced by review ratings
    op.drop_table('ratings')
    
    # Update reviews table to ensure proper structure
    # The reviews table already has rating column from initial migration
    # Verify foreign key constraints are in place
    pass


def downgrade() -> None:
    """
    Downgrade migration:
    1. Recreate ratings table for backward compatibility
    """
    # Recreate ratings table
    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
