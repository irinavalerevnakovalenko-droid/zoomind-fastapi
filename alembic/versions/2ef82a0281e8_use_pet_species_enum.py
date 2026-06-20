"""use pet species enum

Revision ID: 2ef82a0281e8
Revises: c9d8839ae636
Create Date: 2026-06-16 13:49:00.480990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ef82a0281e8'
down_revision: Union[str, Sequence[str], None] = 'c9d8839ae636'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pet_species_enum = sa.Enum(
        'dog',
        'cat',
        'parrot',
        'other',
        name='petspecies',
    )
    pet_species_enum.create(op.get_bind(), checkfirst=True)

    op.execute(
        """
        ALTER TABLE pets
        ALTER COLUMN species TYPE petspecies
        USING species::petspecies
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        ALTER TABLE pets
        ALTER COLUMN species TYPE VARCHAR(20)
        USING species::text
        """
    )

    pet_species_enum = sa.Enum(
        'dog',
        'cat',
        'parrot',
        'other',
        name='petspecies',
    )
    pet_species_enum.drop(op.get_bind(), checkfirst=True)
