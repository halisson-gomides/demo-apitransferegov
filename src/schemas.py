from pydantic import BaseModel


class DefaultMessage(BaseModel):
    message: str


class PdaListOutput(BaseModel):
    plano_acao_id: int
    plano_acao_codigo: str
    plano_acao_ano: int
    plano_acao_situacao: str
    plano_acao_areas_politicas: str | None = None
    beneficiario_cnpj: str
    beneficiario_nome: str
    beneficiario_uf: str
    plano_acao_valor_custeio: float | None = None
    plano_acao_valor_investimento: float | None = None
    parlamentar_nome: str
    parlamentar_numero_emenda: str | None = None


class PdaStatsOutput(BaseModel):
    por_uf: dict
    por_ano: dict