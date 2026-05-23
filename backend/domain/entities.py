from datetime import datetime
from enum import Enum


class StatusAgendamento(Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class Agendamento:
    def __init__(
        self,
        id: int,
        data_inicio: datetime,
        data_fim: datetime,
        servico: str,
        status: StatusAgendamento = StatusAgendamento.PENDENTE,
    ):
        if data_fim <= data_inicio:
            raise ValueError("Data fim deve ser maior que data início")
        
        self.id = id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.servico = servico
        self.status = status

class TipoPerfil(Enum):
    CLIENTE = "cliente"
    CUIDADOR = "cuidador"


class Usuario:
    def __init__(
        self,
        id: int,
        nome: str,
        email: str,
        senha: str,
        tipo: TipoPerfil,
    ):
        if not nome.strip():
            raise ValueError("Nome não pode ser vazio")
        if "@" not in email:
            raise ValueError("Email inválido")
        if len(senha) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")

        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo


class Servico:
    def __init__(
        self,
        id: int,
        nome: str,
        descricao: str,
        cuidador_id: int,
    ):
        if not nome.strip():
            raise ValueError("Nome do serviço não pode ser vazio")

        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.cuidador_id = cuidador_id


class Avaliacao:
    def __init__(
        self,
        id: int,
        agendamento_id: int,
        nota: int,
        comentario: str = "",
    ):
        if nota < 1 or nota > 5:
            raise ValueError("Nota deve ser entre 1 e 5")

        self.id = id
        self.agendamento_id = agendamento_id
        self.nota = nota
        self.comentario = comentario