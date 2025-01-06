from sqlmodel import Field, SQLModel


class PlanoAcaoEspecial(SQLModel, table=True):
    __tablename__ = "tab_plano_acao_especial"

    id_plano_acao: int | None = Field(default=None, primary_key=True)
    codigo_plano_acao: str | None
    ano_plano_acao: int | None
    modalidade_plano_acao: str | None
    situacao_plano_acao: str | None
    cnpj_beneficiario_plano_acao: str | None
    nome_beneficiario_plano_acao: str | None
    uf_beneficiario_plano_acao: str | None
    codigo_banco_plano_acao: str | None
    codigo_situacao_dado_bancario_plano_acao: float | None
    nome_banco_plano_acao: str | None
    numero_agencia_plano_acao: float | None
    dv_agencia_plano_acao: str | None
    numero_conta_plano_acao: float | None
    dv_conta_plano_acao: str | None
    nome: str | None
    ano_emenda_parlamentar_plano_acao: str | None
    codigo_parlamentar_emenda_plano_acao: str | None
    sequencial_emenda_parlamentar_plano_acao: int | None
    numero_emenda_parlamentar_plano_acao: str | None
    codigo_emenda_parlamentar_formatado_plano_acao: str | None
    codigo_descricao_areas_politicas_publicas_plano_acao: str | None
    descricao_programacao_orcamentaria_plano_acao: str | None
    motivo_impedimento_plano_acao: str | None
    valor_custeio_plano_acao: float | None
    valor_investimento_plano_acao: float | None
    id_programa: int | None