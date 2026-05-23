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

from domain.entities import Usuario, Servico, Avaliacao, TipoPerfil


def test_usuario_valido():
    usuario = Usuario(
        id=1,
        nome="João Silva",
        email="joao@email.com",
        senha="123456",
        tipo=TipoPerfil.CLIENTE,
    )
    assert usuario.tipo == TipoPerfil.CLIENTE
    print("✅ Usuário válido criado com sucesso!")


def test_usuario_email_invalido():
    try:
        Usuario(
            id=2,
            nome="Maria",
            email="emailinvalido",
            senha="123456",
            tipo=TipoPerfil.CUIDADOR,
        )
        print("❌ Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Erro capturado: {e}")


def test_usuario_senha_curta():
    try:
        Usuario(
            id=3,
            nome="Pedro",
            email="pedro@email.com",
            senha="123",
            tipo=TipoPerfil.CLIENTE,
        )
        print("❌ Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Erro capturado: {e}")


def test_avaliacao_nota_invalida():
    try:
        Avaliacao(
            id=1,
            agendamento_id=1,
            nota=6,
        )
        print("❌ Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Erro capturado: {e}")


def test_servico_valido():
    servico = Servico(
        id=1,
        nome="Acompanhamento diário",
        descricao="Cuidado diário ao paciente",
        cuidador_id=1,
    )
    assert servico.nome == "Acompanhamento diário"
    print("✅ Serviço válido criado com sucesso!")


test_usuario_valido()
test_usuario_email_invalido()
test_usuario_senha_curta()
test_avaliacao_nota_invalida()
test_servico_valido()
