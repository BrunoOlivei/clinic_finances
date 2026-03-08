from typing import Optional

from src.core import logger
from src.services import (
    AtendimentosSaoLucasBronze,
    AtendimentosSaoLucasSilver,
    SolicitacoesSaoLucasBronze,
    SolicitacoesSaoLucasSilver,
    RecibosSaoLucasBronze,
)


class Pipeline:
    def __init__(self, dt_base: int, pipeline_name: Optional[str] = None) -> None:
        self.dt_base = dt_base
        self.pipeline_name = pipeline_name

    def pipeline_atendimento_sao_lucas(self) -> bool:
        bronze_finished = AtendimentosSaoLucasBronze(dt_base=self.dt_base).main()
        if bronze_finished:
            silver_finished = AtendimentosSaoLucasSilver(dt_base=self.dt_base).main()
            return silver_finished
        else:
            return False

    def pipeline_solicitacoes_sao_lucas(self) -> bool:
        bronze_finished = SolicitacoesSaoLucasBronze(dt_base=self.dt_base).main()
        if bronze_finished:
            silver_finished = SolicitacoesSaoLucasSilver(dt_base=self.dt_base).main()
            return silver_finished
        else:
            return False

    def pipeline_recibos_sao_lucas(self) -> bool:
        bronze_finished = RecibosSaoLucasBronze(dt_base=self.dt_base).main()
        return bronze_finished

    def run_all_pipelines(self):
        pipeline_atendimento = self.pipeline_atendimento_sao_lucas()
        if pipeline_atendimento:
            logger.info("ATENDIMENTO SAO LUCAS PIPELINE RUN SUCESSFULY")

        pipeline_solicitacoes = self.pipeline_solicitacoes_sao_lucas()
        if pipeline_solicitacoes:
            logger.info("SOLICITACOES SAO LUCAS PIPELINE RUN SUCESSFULY")

        pipeline_recibos = self.pipeline_recibos_sao_lucas()
        if pipeline_recibos:
            logger.info("RECIBOS SAO LUCAS PIPELINE RUN SUCESSFULY")

    def run(self):
        if self.pipeline_name == "atendimento":
            pipeline_atendimento = self.pipeline_atendimento_sao_lucas()
            if pipeline_atendimento:
                logger.info("ATENDIMENTO SAO LUCAS PIPELINE RUN SUCESSFULY")
        elif self.pipeline_name == "solicitacao":
            pipeline_solicitacoes = self.pipeline_solicitacoes_sao_lucas()
            if pipeline_solicitacoes:
                logger.info("SOLICITACOES SAO LUCAS PIPELINE RUN SUCESSFULY")
        elif self.pipeline_name == "recibos":
            pipeline_recibos = self.pipeline_recibos_sao_lucas()
            if pipeline_recibos:
                logger.info("RECIBOS SAO LUCAS PIPELINE RUN SUCESSFULY")
        else:
            logger.error(f"Pipeline_name not supported: {self.pipeline_name}")


if __name__ == "__main__":
    Pipeline(dt_base=202601, pipeline_name="recibos").run()
