# trigger cron
import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage

# =========================
# API
# =========================
url = "https://api.ifollower.com.br/statistic/opened-report"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTQxNSwicGVyZmlsIjoiQkkiLCJlbXByZXNhIjo2LCJpYXQiOjE3NTA0MjczNDEsImV4cCI6MTc4MTk4NDk0MX0.UrJiYQUm_hmUBMPelcBcGyctDT2ziIllNX5W8JXZETU",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

# =========================
# Ajuste do JSON
# =========================
if isinstance(data, dict):
    encontrou_lista = False
    for key in data:
        if isinstance(data[key], list):
            df = pd.json_normalize(data[key])
            encontrou_lista = True
            break

    if not encontrou_lista:
        df = pd.json_normalize(data)
else:
    df = pd.json_normalize(data)

# =========================
# CSV
# =========================
hoje = datetime.now().strftime("%Y-%m-%d_%H-%M")
arquivo = f"relatorio_opened_{hoje}.csv"

df.to_csv(arquivo, index=False, encoding="utf-8-sig")

# =========================
# EMAIL (GMAIL)
# =========================
EMAIL_REMETENTE = "pedro.donpe777@gmail.com"
EMAIL_SENHA = "puro rsei ject uwpw"
EMAIL_DESTINO = "pedro.silva@craneww.com"

msg = EmailMessage()
msg["Subject"] = "Relatório Opened Report"
msg["From"] = EMAIL_REMETENTE
msg["To"] = EMAIL_DESTINO
msg.set_content("Segue em anexo o relatório gerado automaticamente.")

# Anexo CSV
with open(arquivo, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="text",
        subtype="csv",
        filename=arquivo
    )

# Envio via Gmail SMTP
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
    smtp.send_message(msg)

print("✅ CSV gerado e enviado com sucesso!")
