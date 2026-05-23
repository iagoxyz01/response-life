from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infrastructure.database import get_db
from infrastructure.models import ServicoModel, UsuarioModel, TipoPerfil
from dependencies import get_usuario_atual

router = APIRouter(prefix="/servicos", tags=["Serviços"])


class ServicoCreate(BaseModel):
    nome: str
    descricao: str


class ServicoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    cuidador_id: int

    class Config:
        from_attributes = True


@router.post("/", response_model=ServicoResponse)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    # Apenas cuidadores podem cadastrar serviços
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores podem cadastrar serviços"
        )

    novo_servico = ServicoModel(
        nome=servico.nome,
        descricao=servico.descricao,
        cuidador_id=usuario_atual.id,
    )
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico


@router.get("/", response_model=list[ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoModel).all()


@router.get("/meus", response_model=list[ServicoResponse])
def meus_servicos(
    db: Session = Depends(get_db),
    usuario_atual: UsuarioModel = Depends(get_usuario_atual),
):
    if usuario_atual.tipo != TipoPerfil.CUIDADOR:
        raise HTTPException(
            status_code=403,
            detail="Apenas cuidadores têm serviços"
        )

    return db.query(ServicoModel).filter(
        ServicoModel.cuidador_id == usuario_atual.id
    ).all()