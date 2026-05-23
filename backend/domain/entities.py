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