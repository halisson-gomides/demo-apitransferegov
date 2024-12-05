from sqlmodel import Field, SQLModel, Field


class PlanoAcaoEspecial(SQLModel, table=True):
    __tablename__ = "tab_plano_acao_especial"

    id_plano_acao: int | None = Field(default=None, primary_key=True)
    codigo_plano_acao: str
    ano_plano_acao: int
    modalidade_plano_acao: str
    situacao_plano_acao: str
    cnpj_beneficiario_plano_acao: str
    nome_beneficiario_plano_acao: str
    uf_beneficiario_plano_acao: str
    codigo_banco_plano_acao: str
    codigo_situacao_dado_bancario_plano_acao: float
    nome_banco_plano_acao: str
    numero_agencia_plano_acao: float
    dv_agencia_plano_acao: str
    numero_conta_plano_acao: float
    dv_conta_plano_acao: str
    nome: str
    ano_emenda_parlamentar_plano_acao: str
    codigo_parlamentar_emenda_plano_acao: str
    sequencial_emenda_parlamentar_plano_acao: int
    numero_emenda_parlamentar_plano_acao: str
    codigo_emenda_parlamentar_formatado_plano_acao: str
    codigo_descricao_areas_politicas_publicas_plano_acao: str
    descricao_programacao_orcamentaria_plano_acao: str
    motivo_impedimento_plano_acao: str
    valor_custeio_plano_acao: float
    valor_investimento_plano_acao: float
    id_programa: int