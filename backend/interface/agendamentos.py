from sqlalchemy import exists
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from infrastructure.database import get_db
from infrastructure.models import (
    AgendamentoModel,
    ServicoModel,
    UsuarioModel,
    TipoPerfil,
    StatusAgendamento,
)
from dependencies import get_usuario_atual

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


class AgendamentoCreate(BaseModel):
    data_inicio: datetime
    data_fim: datetime
    servico_id: int


class AgendamentoResponse(BaseModel):
    id: int
    data_inicio: datetime
    data_fim: datetime
    servico_id: int
    cliente_id: int
    status: StatusAgendamento
    avaliado: bool = False

    class Config:
        from_attributes = True


@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    agendamento: AgendamentoCreate,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    # Apenas clientes podem agendar
    if usuario_atual.tipo != TipoPerfil.CLIENTE:
        raise HTTPException(
            status_code=403,
            detail="Apenas clientes podem criar agendamentos"
        )

    # Verificar se data fim é maior que data início
    if agendamento.data_fim <= agendamento.data_inicio:
        raise HTTPException(
            status_code=400,
            detail="Data fim deve ser maior que data início"
        )

    # Verificar se serviço existe
    servico = db.query(ServicoModel).filter(
        ServicoModel.id == agendamento.servico_id
    ).first()
    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    novo_agendamento = AgendamentoModel(
        data_inicio=agendamento.data_inicio,
        data_fim=agendamento.data_fim,
        servico_id=agendamento.servico_id,
        cliente_id=usuario_atual.id,
        status=StatusAgendamento.PENDENTE,
    )
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)

    return novo_agendamento


@router.get("/meus", response_model=list[AgendamentoResponse])
def meus_agendamentos(
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    from infrastructure.models import AvaliacaoModel

    if usuario_atual.tipo == TipoPerfil.CLIENTE:
        agendamentos = db.query(AgendamentoModel).filter(
            AgendamentoModel.cliente_id == usuario_atual.id
        ).all()
    else:
        agendamentos = db.query(AgendamentoModel).join(ServicoModel).filter(
            ServicoModel.cuidador_id == usuario_atual.id
        ).all()

    resultado = []
    for ag in agendamentos:
        avaliado = db.query(AvaliacaoModel).filter(
            AvaliacaoModel.agendamento_id == ag.id
        ).first() is not None
        
        item = AgendamentoResponse(
            id=ag.id,
            data_inicio=ag.data_inicio,
            data_fim=ag.data_fim,
            servico_id=ag.servico_id,
            cliente_id=ag.cliente_id,
            status=ag.status,
            avaliado=avaliado,
        )
        resultado.append(item)

    return resultado

@router.patch("/{agendamento_id}/concluir", response_model=AgendamentoResponse)
def concluir_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores podem concluir agendamentos"
        )

    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    agendamento.status = StatusAgendamento.CONCLUIDO
    db.commit()
    db.refresh(agendamento)

    return agendamento


@router.patch("/{agendamento_id}/cancelar", response_model=AgendamentoResponse)
def cancelar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status != StatusAgendamento.PENDENTE:
        raise HTTPException(
            status_code=400,
            detail="Apenas agendamentos pendentes podem ser cancelados"
        )

    agendamento.status = StatusAgendamento.CANCELADO
    db.commit()
    db.refresh(agendamento)

    return agendamento

@router.patch("/{agendamento_id}/aceitar", response_model=AgendamentoResponse)
def aceitar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores podem aceitar agendamentos"
        )

    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status != StatusAgendamento.PENDENTE:
        raise HTTPException(
            status_code=400,
            detail="Apenas agendamentos pendentes podem ser aceitos"
        )

    agendamento.status = StatusAgendamento.ACEITO
    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.patch("/{agendamento_id}/recusar", response_model=AgendamentoResponse)
def recusar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores podem recusar agendamentos"
        )

    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    agendamento.status = StatusAgendamento.RECUSADO
    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.patch("/{agendamento_id}/iniciar", response_model=AgendamentoResponse)
def iniciar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores podem iniciar agendamentos"
        )

    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status != StatusAgendamento.ACEITO:
        raise HTTPException(
            status_code=400,
            detail="Apenas agendamentos aceitos podem ser iniciados"
        )

    agendamento.status = StatusAgendamento.ATIVO
    db.commit()
    db.refresh(agendamento)
    return agendamento