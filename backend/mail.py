import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def enviar_email_recuperacao(email: str, token: str):
    link = f"https://response-life-gamma.vercel.app/nova-senha?token={token}"

    resend.Emails.send({
        "from": "Response Life <onboarding@resend.dev>",
        "to": [email],
        "subject": "Recuperação de senha - Response Life",
        "html": f"""
        <h2>Recuperação de senha</h2>
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <a href="{link}">{link}</a>
        <p>O link expira em 30 minutos.</p>
        <p>Se você não solicitou a recuperação, ignore este email.</p>
        """,
    })