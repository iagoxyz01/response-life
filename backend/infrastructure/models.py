from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from infrastructure.database import Base
import enum


class StatusAgendamento(enum.Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class TipoPerfil(enum.Enum):
    CLIENTE = "cliente"
    CUIDADOR = "cuidador"


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    tipo = Column(Enum(TipoPerfil), nullable=False)


class ServicoModel(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    cuidador_id = Column(Integer, ForeignKey("usuarios.id"))


class AgendamentoModel(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)


class AvaliacaoModel(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"))
    nota = Column(Integer, nullable=False)
    comentario = Column(String, default="")