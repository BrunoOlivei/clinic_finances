#%%
from src.services import (
    AtendimentosSaoLucasBronze,
    AtendimentosSaoLucasSilver
)
from src.core import logger


class Pipeline:
    def __init__(self, dt_base: int) -> None:
        self.dt_base = dt_base

    def pipeline_atendimento_sao_lucas(self) -> bool:
        bronze_finished = AtendimentosSaoLucasBronze(
            dt_base=self.dt_base
        ).main()
        if bronze_finished:
            silver_finished = AtendimentosSaoLucasSilver(
                dt_base=self.dt_base
            ).main()
        return silver_finished

    def run(self):
        pipeline_atendimento = self.pipeline_atendimento_sao_lucas()
        if pipeline_atendimento:
            logger.info("ATENDIMENTO SAO LUCAS PIPELINE RUN SUCESSFULY")


if __name__ == "__main__":
    Pipeline(
        dt_base=202507
    ).run()


#%%
# obj = AtendimentosSaoLucasSilver(
#     dt_base=202507
# )
# df = obj.main()
# print(df.iloc[0, 0])

