from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    # username of the email address sending the emails
    MAIL_USERNAME=Config.MAIL_USERNAME,
    # password for the SMTP server
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    # The email address of the sender
    MAIL_FROM=Config.MAIL_FROM,
    # The port used to connect to the SMTP server (usually 587 for TLS).
    MAIL_PORT=587,
    # The SMTP server used to send emails
    MAIL_SERVER=Config.MAIL_SERVER,
    # The name displayed as the sender of the email
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    # Enables the STARTTLS command, upgrades connection to TLS/SSL
    MAIL_STARTTLS=True,
    # Indicates whether to use SSL/TLS for the connection from the start.
    MAIL_SSL_TLS=False,
    # Specifies whether to use credentials to authenticate with the SMTP Server
    USE_CREDENTIALS=True,
    # Specifies whether to validate the server's SSL certificates
    VALIDATE_CERTS=True,
    # Specifies the folder containing email templates, useful to sending HTML emails with Jinja Templates.
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")
)

mail = FastMail(config=mail_config)

def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    
    return message