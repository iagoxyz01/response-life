from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infrastructure.database import get_db
from infrastructure.models import AvaliacaoModel, AgendamentoModel, StatusAgendamento, UsuarioModel
from dependencies import get_usuario_atual

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


class AvaliacaoCreate(BaseModel):
    agendamento_id: int
    nota: int
    comentario: str = ""


class AvaliacaoResponse(BaseModel):
    id: int
    agendamento_id: int
    nota: int
    comentario: str

    class Config:
        from_attributes = True


@router.post("/", response_model=AvaliacaoResponse)
def criar_avaliacao(
    avaliacao: AvaliacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    agendamento = db.query(AgendamentoModel).filter(
        AgendamentoModel.id == avaliacao.agendamento_id
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status != StatusAgendamento.CONCLUIDO:
        raise HTTPException(
            status_code=400,
            detail="Só é possível avaliar agendamentos concluídos"
        )

    # Verificar se já foi avaliado
    avaliacao_existente = db.query(AvaliacaoModel).filter(
        AvaliacaoModel.agendamento_id == avaliacao.agendamento_id
    ).first()

    if avaliacao_existente:
        raise HTTPException(
            status_code=400,
            detail="Este agendamento já foi avaliado"
        )

    if avaliacao.nota < 1 or avaliacao.nota > 5:
        raise HTTPException(
            status_code=400,
            detail="Nota deve ser entre 1 e 5"
        )

    nova_avaliacao = AvaliacaoModel(
        agendamento_id=avaliacao.agendamento_id,
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
    )
    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return nova_avaliacao
