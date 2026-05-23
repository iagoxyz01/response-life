from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from infrastructure.database import get_db
from infrastructure.models import UsuarioModel, TipoPerfil
from passlib.context import CryptContext

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: TipoPerfil


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    tipo: TipoPerfil

    class Config:
        from_attributes = True


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Criptografar senha
    senha_hash = pwd_context.hash(usuario.senha)

    # Criar usuário no banco
    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash,
        tipo=usuario.tipo,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario