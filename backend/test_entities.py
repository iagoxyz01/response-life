from datetime import datetime
from domain.entities import Agendamento, StatusAgendamento


def test_agendamento_valido():
    agendamento = Agendamento(
        id=1,
        data_inicio=datetime(2026, 6, 1, 8, 0),
        data_fim=datetime(2026, 6, 1, 10, 0),
        servico="Banho e tosa",
    )
    assert agendamento.status == StatusAgendamento.PENDENTE
    print("✅ Agendamento válido criado com sucesso!")


def test_agendamento_data_invalida():
    try:
        agendamento = Agendamento(
            id=2,
            data_inicio=datetime(2026, 6, 1, 10, 0),
            data_fim=datetime(2026, 6, 1, 8, 0),
            servico="Consulta",
        )
        print("❌ Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Erro capturado corretamente: {e}")


test_agendamento_valido()
test_agendamento_data_invalida()