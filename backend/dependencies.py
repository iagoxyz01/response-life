from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.models import UsuarioModel
from auth import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")


def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UsuarioModel:
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    return usuario