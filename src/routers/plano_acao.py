from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import PdaListOutput, PdaStatsOutput, DefaultMessage
from src.database import get_session
from src.models import PlanoAcaoEspecial

from typing import Optional, List
from sqlalchemy import or_



pda_router = APIRouter(prefix="/plano_acao")

@pda_router.get('/id/{plano_id}', 
                status_code=HTTPStatus.OK,
                response_model=PdaListOutput,
                description="Lista Plano de Ação por ID")
async def read_plano_acao_by_id(plano_id:int, session:AsyncSession=Depends(get_session)):
    
        query = select(PlanoAcaoEspecial).where(PlanoAcaoEspecial.id_plano_acao == plano_id)
        result = await session.execute(query)
        plano = result.scalar_one_or_none()
        if not plano:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Plano não econtrado")
        
        return {            
                "plano_acao_id": plano.id_plano_acao,
                "plano_acao_codigo": plano.codigo_plano_acao,
                "plano_acao_ano": plano.ano_plano_acao,
                "plano_acao_situacao": plano.situacao_plano_acao,
                "plano_acao_areas_politicas": plano.codigo_descricao_areas_politicas_publicas_plano_acao,
                "beneficiario_cnpj": plano.cnpj_beneficiario_plano_acao,
                "beneficiario_nome": plano.nome_beneficiario_plano_acao,
                "beneficiario_uf": plano.uf_beneficiario_plano_acao,
                "parlamentar_nome": plano.nome,
                "parlamentar_numero_emenda": plano.numero_emenda_parlamentar_plano_acao,
        }


@pda_router.get('/search/',
                status_code=HTTPStatus.OK,
                response_model=List[PdaListOutput],    
                description="Pesquisa Planos de Ação pela combinação de critérios"                 
                )
async def pesquisa_planos(
     ano: Optional[int]=None,
     uf: Optional[str]=None,
     muni_beneficiario: Optional[str] = None,
     session:AsyncSession = Depends(get_session)
):
    try:     
        query = select(PlanoAcaoEspecial)

        if not any([ano, uf, muni_beneficiario]):
            raise

        if ano:
            query = query.where(PlanoAcaoEspecial.ano_plano_acao == ano)    
        if uf:
            query = query.where(PlanoAcaoEspecial.uf_beneficiario_plano_acao == uf.upper())
        if muni_beneficiario:
            query = query.where(PlanoAcaoEspecial.nome_beneficiario_plano_acao.ilike(f"%{muni_beneficiario}%"))

        result = await session.execute(query)
        planos = result.scalars().all()
    except Exception as err:
         raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Parâmetros de consulta inválidos.")
    
    return [{            
                "plano_acao_id": plano.id_plano_acao,
                "plano_acao_codigo": plano.codigo_plano_acao,
                "plano_acao_ano": plano.ano_plano_acao,
                "plano_acao_situacao": plano.situacao_plano_acao,
                "plano_acao_areas_politicas": plano.codigo_descricao_areas_politicas_publicas_plano_acao,
                "beneficiario_cnpj": plano.cnpj_beneficiario_plano_acao,
                "beneficiario_nome": plano.nome_beneficiario_plano_acao,
                "beneficiario_uf": plano.uf_beneficiario_plano_acao,
                "parlamentar_nome": plano.nome,
                "parlamentar_numero_emenda": plano.numero_emenda_parlamentar_plano_acao,
        } for plano in planos]
    
     


@pda_router.get('/stats/', 
                status_code=HTTPStatus.OK,
                response_model=PdaStatsOutput,
                description="Lista Quantitativos por UF e por Ano")
async def read_planos_stats(session:AsyncSession=Depends(get_session)):
    from sqlalchemy import func
    # Contagem por UF
    query_uf = select(
        PlanoAcaoEspecial.uf_beneficiario_plano_acao,
        func.count(PlanoAcaoEspecial.id_plano_acao)
    ).group_by(PlanoAcaoEspecial.uf_beneficiario_plano_acao)
    
    # Contagem por ano
    query_ano = select(
        PlanoAcaoEspecial.ano_plano_acao,
        func.count(PlanoAcaoEspecial.id_plano_acao)
    ).group_by(PlanoAcaoEspecial.ano_plano_acao)

    result_uf = await session.execute(query_uf)
    result_ano = await session.execute(query_ano)
    
    return {
        "por_uf": dict(result_uf.all()),
        "por_ano": dict(result_ano.all())
    }