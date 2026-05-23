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
from auth import verificar_senha, criar_token
from fastapi.security import OAuth2PasswordRequestForm


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuário pelo email
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # Verificar senha
    if not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    # Gerar token
    token = criar_token({"sub": usuario.email, "tipo": usuario.tipo.value})

    return {"access_token": token, "token_type": "bearer"}