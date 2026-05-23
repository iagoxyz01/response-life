from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface import usuarios, servicos, agendamentos

app = FastAPI(
    title="Response Life API",
    description="API do app de agendamento de cuidadores",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(servicos.router)
app.include_router(agendamentos.router)


@app.get("/")
def root():
    return {"mensagem": "Response Life API funcionando! 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}