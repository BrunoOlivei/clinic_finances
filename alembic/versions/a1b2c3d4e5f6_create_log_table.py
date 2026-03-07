"""create log table

Revision ID: a1b2c3d4e5f6
Revises: 1cd4d59573b9
Create Date: 2026-03-07 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '1cd4d59573b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS log")
    op.create_table(
        'tb_logs',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, comment='Identificador único do log (UUID)'),
        sa.Column('level', sa.String(length=20), nullable=False, comment='Nível do log (ex: WARNING, ERROR, CRITICAL)'),
        sa.Column('message', sa.Text(), nullable=False, comment='Mensagem do log'),
        sa.Column('module', sa.String(length=255), nullable=True, comment='Módulo onde o log foi gerado'),
        sa.Column('function', sa.String(length=255), nullable=True, comment='Função onde o log foi gerado'),
        sa.Column('line', sa.Integer(), nullable=True, comment='Linha do código onde o log foi gerado'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='Data e hora de criação do log'),
        sa.PrimaryKeyConstraint('id', name='pk_tb_logs'),
        schema='log',
        comment='Tabela de logs da aplicação',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tb_logs', schema='log')
