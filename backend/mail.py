from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def enviar_email_recuperacao(email: str, token: str):
    link = f"https://response-life-gamma.vercel.app/nova-senha?token={token}"

    mensagem = MessageSchema(
        subject="Recuperação de senha - Response Life",
        recipients=[email],
        body=f"""
        <h2>Recuperação de senha</h2>
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <a href="{link}">{link}</a>
        <p>O link expira em 30 minutos.</p>
        <p>Se você não solicitou a recuperação, ignore este email.</p>
        """,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(mensagem)