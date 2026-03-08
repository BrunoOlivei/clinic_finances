"""reorder procedimento_1 column in tb_solicitacoes_sao_lucas

Revision ID: 32cb5094e56e
Revises: acb95ea1ed3d
Create Date: 2026-03-08 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32cb5094e56e'
down_revision: Union[str, Sequence[str], None] = 'acb95ea1ed3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Reorder procedimento_1 to appear after procedimento and before qtde_sol."""
    op.execute("""
        CREATE TABLE brz.tb_solicitacoes_sao_lucas_new (
            id UUID DEFAULT gen_random_uuid() NOT NULL,
            solicitacao VARCHAR(10) NOT NULL,
            data VARCHAR(19) NOT NULL,
            validade_solicitacao VARCHAR(10) NOT NULL,
            solicitante VARCHAR(5) NOT NULL,
            operador VARCHAR(255) NOT NULL,
            terminal VARCHAR(255),
            solicitante_1 VARCHAR(255) NOT NULL,
            beneficiario VARCHAR(18) NOT NULL,
            beneficiario_1 VARCHAR(255),
            especialidade VARCHAR(255) NOT NULL,
            procedimento VARCHAR(8) NOT NULL,
            procedimento_1 VARCHAR(255) NOT NULL,
            qtde_sol VARCHAR(3) NOT NULL,
            qtde_lib VARCHAR(3) NOT NULL,
            qtde_exe VARCHAR(3) NOT NULL,
            prestador VARCHAR(255),
            especialidade_prestador VARCHAR(255),
            status VARCHAR(50) NOT NULL,
            especificacao VARCHAR(255),
            tipo_de_solicitacao VARCHAR(255) NOT NULL,
            operador_cancelamento VARCHAR(255),
            observacao VARCHAR(255),
            auditor VARCHAR(255),
            data_agendamento VARCHAR(10),
            operador_agendamento VARCHAR(255),
            dt_base INTEGER NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            silver_exported BOOLEAN NOT NULL DEFAULT FALSE,
            silver_date_export TIMESTAMP,
            CONSTRAINT pk_tb_solicitacoes_sao_lucas_new PRIMARY KEY (id)
        )
    """)

    op.execute("""
        INSERT INTO brz.tb_solicitacoes_sao_lucas_new (
            id, solicitacao, data, validade_solicitacao, solicitante, operador, terminal,
            solicitante_1, beneficiario, beneficiario_1, especialidade, procedimento,
            procedimento_1, qtde_sol, qtde_lib, qtde_exe, prestador, especialidade_prestador,
            status, especificacao, tipo_de_solicitacao, operador_cancelamento, observacao,
            auditor, data_agendamento, operador_agendamento, dt_base, file_name,
            created_at, updated_at, silver_exported, silver_date_export
        )
        SELECT
            id, solicitacao, data, validade_solicitacao, solicitante, operador, terminal,
            solicitante_1, beneficiario, beneficiario_1, especialidade, procedimento,
            procedimento_1, qtde_sol, qtde_lib, qtde_exe, prestador, especialidade_prestador,
            status, especificacao, tipo_de_solicitacao, operador_cancelamento, observacao,
            auditor, data_agendamento, operador_agendamento, dt_base, file_name,
            created_at, updated_at, silver_exported, silver_date_export
        FROM brz.tb_solicitacoes_sao_lucas
    """)

    op.execute("DROP TABLE brz.tb_solicitacoes_sao_lucas")
    op.execute("ALTER TABLE brz.tb_solicitacoes_sao_lucas_new RENAME TO tb_solicitacoes_sao_lucas")
    op.execute("ALTER TABLE brz.tb_solicitacoes_sao_lucas RENAME CONSTRAINT pk_tb_solicitacoes_sao_lucas_new TO pk_tb_solicitacoes_sao_lucas")

    op.execute("""
        COMMENT ON TABLE brz.tb_solicitacoes_sao_lucas IS
        'Tabela de solicitações importadas da operadora São Lucas, na camada bronze'
    """)
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.id IS 'Identificador único do registro (UUID)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.solicitacao IS 'Número da solicitação.'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.data IS 'Data da abertura da solicitação (formato: dd/mm/yyyy)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.validade_solicitacao IS 'Data do vencimento da solicitação (formato: dd/mm/yyyy)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.solicitante IS 'Código do profissinal de saúde solicitante'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.operador IS 'Código do usuário que registrou a solicitação no sistema'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.terminal IS 'Nome do usuário master do sistema para identificação de onde partiu a solicitação'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.solicitante_1 IS 'Nome do profissional de saúde solicitante'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.beneficiario IS 'Código do beneficiário (código do paciente)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.beneficiario_1 IS 'Nome do beneficiário (nome do paciente)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.especialidade IS 'Especialidade do profissional de saúde solicitante'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.procedimento IS 'Código do procedimento solicitado'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.procedimento_1 IS 'Nome do procedimento solicitado'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.qtde_sol IS 'Quantidade do procedimento solicitado'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.qtde_lib IS 'Quantidade do procedimento solicitado que foi liberado pela operadora'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.qtde_exe IS 'Quantidade do procedimento solicitado que foi executado'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.prestador IS 'Código do prestador (código do profissional ou instituição que realizou o procedimento)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.especialidade_prestador IS 'Especialidade do prestador que executou o procedimento solicitado'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.status IS 'Descrição do status da solicitação'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.especificacao IS 'Descrições de especificações e orientações relacionadas ao procedimento solicitado, se disponíveis'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.tipo_de_solicitacao IS 'Tipo de solicitação (ex: Consulta, Exame)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.operador_cancelamento IS 'Código do operador que cancelou a solicitação, se aplicável'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.observacao IS 'Observações sobre a solicitação'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.auditor IS 'Código do usuário que realizou a auditoria da solicitação, se disponível'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.data_agendamento IS 'Data de agendamento para a realização do procedimento solicitado, se disponível (formato: dd/mm/yyyy)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.operador_agendamento IS 'Código do operador que realizou o agendamento, se disponível'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.dt_base IS 'Mês e ano base do arquivo no formato YYYYMM (ex: 202401)'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.file_name IS 'Nome do arquivo de origem do atendimento'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.created_at IS 'Data e hora de criação do registro'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.updated_at IS 'Data e hora de última atualização do registro'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.silver_exported IS 'Flag indicando se o registro foi exportado para a camada silver'")
    op.execute("COMMENT ON COLUMN brz.tb_solicitacoes_sao_lucas.silver_date_export IS 'Data e hora de exportação para a camada silver'")


def downgrade() -> None:
    """Move procedimento_1 back to the last position (before control columns)."""
    op.execute("""
        CREATE TABLE brz.tb_solicitacoes_sao_lucas_new (
            id UUID DEFAULT gen_random_uuid() NOT NULL,
            solicitacao VARCHAR(10) NOT NULL,
            data VARCHAR(19) NOT NULL,
            validade_solicitacao VARCHAR(10) NOT NULL,
            solicitante VARCHAR(5) NOT NULL,
            operador VARCHAR(255) NOT NULL,
            terminal VARCHAR(255),
            solicitante_1 VARCHAR(255) NOT NULL,
            beneficiario VARCHAR(18) NOT NULL,
            beneficiario_1 VARCHAR(255),
            especialidade VARCHAR(255) NOT NULL,
            procedimento VARCHAR(8) NOT NULL,
            qtde_sol VARCHAR(3) NOT NULL,
            qtde_lib VARCHAR(3) NOT NULL,
            qtde_exe VARCHAR(3) NOT NULL,
            prestador VARCHAR(255),
            especialidade_prestador VARCHAR(255),
            status VARCHAR(50) NOT NULL,
            especificacao VARCHAR(255),
            tipo_de_solicitacao VARCHAR(255) NOT NULL,
            operador_cancelamento VARCHAR(255),
            observacao VARCHAR(255),
            auditor VARCHAR(255),
            data_agendamento VARCHAR(10),
            operador_agendamento VARCHAR(255),
            dt_base INTEGER NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            silver_exported BOOLEAN NOT NULL DEFAULT FALSE,
            silver_date_export TIMESTAMP,
            procedimento_1 VARCHAR(255) NOT NULL,
            CONSTRAINT pk_tb_solicitacoes_sao_lucas_new PRIMARY KEY (id)
        )
    """)

    op.execute("""
        INSERT INTO brz.tb_solicitacoes_sao_lucas_new (
            id, solicitacao, data, validade_solicitacao, solicitante, operador, terminal,
            solicitante_1, beneficiario, beneficiario_1, especialidade, procedimento,
            qtde_sol, qtde_lib, qtde_exe, prestador, especialidade_prestador,
            status, especificacao, tipo_de_solicitacao, operador_cancelamento, observacao,
            auditor, data_agendamento, operador_agendamento, dt_base, file_name,
            created_at, updated_at, silver_exported, silver_date_export, procedimento_1
        )
        SELECT
            id, solicitacao, data, validade_solicitacao, solicitante, operador, terminal,
            solicitante_1, beneficiario, beneficiario_1, especialidade, procedimento,
            qtde_sol, qtde_lib, qtde_exe, prestador, especialidade_prestador,
            status, especificacao, tipo_de_solicitacao, operador_cancelamento, observacao,
            auditor, data_agendamento, operador_agendamento, dt_base, file_name,
            created_at, updated_at, silver_exported, silver_date_export, procedimento_1
        FROM brz.tb_solicitacoes_sao_lucas
    """)

    op.execute("DROP TABLE brz.tb_solicitacoes_sao_lucas")
    op.execute("ALTER TABLE brz.tb_solicitacoes_sao_lucas_new RENAME TO tb_solicitacoes_sao_lucas")
    op.execute("ALTER TABLE brz.tb_solicitacoes_sao_lucas RENAME CONSTRAINT pk_tb_solicitacoes_sao_lucas_new TO pk_tb_solicitacoes_sao_lucas")
