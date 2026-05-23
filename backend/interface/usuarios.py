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

from mail import enviar_email_recuperacao
from datetime import datetime, timedelta
import secrets


class RecuperarSenhaRequest(BaseModel):
    email: str


class NovaSenhaRequest(BaseModel):
    token: str
    nova_senha: str


@router.post("/recuperar-senha")
async def recuperar_senha(
    request: RecuperarSenhaRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == request.email
    ).first()

    if not usuario:
        # Por segurança não revelamos se o email existe
        return {"mensagem": "Se o email existir, você receberá as instruções"}

    # Gerar token único
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(minutes=30)

    usuario.reset_token = token
    usuario.reset_token_expiry = expiry
    db.commit()

    # Enviar email
    await enviar_email_recuperacao(usuario.email, token)

    return {"mensagem": "Se o email existir, você receberá as instruções"}


@router.post("/nova-senha")
def nova_senha(
    request: NovaSenhaRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.reset_token == request.token
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Token inválido")

    if usuario.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")

    if len(request.nova_senha) < 6:
        raise HTTPException(
            status_code=400,
            detail="Senha deve ter no mínimo 6 caracteres"
        )

    usuario.senha = pwd_context.hash(request.nova_senha)
    usuario.reset_token = None
    usuario.reset_token_expiry = None
    db.commit()

    return {"mensagem": "Senha alterada com sucesso!"}