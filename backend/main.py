from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface import usuarios, servicos, agendamentos, avaliacoes

app = FastAPI(
    title="Response Life API",
    description="API do app de agendamento de cuidadores",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(servicos.router)
app.include_router(agendamentos.router)
app.include_router(avaliacoes.router)


@app.on_event("startup")
def startup():
    from infrastructure.database import engine, Base
    from infrastructure import models
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas/verificadas!")


@app.get("/")
def root():
    return {"mensagem": "Response Life API funcionando! 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}