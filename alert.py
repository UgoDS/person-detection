import smtplib
from dotenv import load_dotenv
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

load_dotenv()


def create_message(
    send_from,
    send_to,
    subject,
    file_path,
):
    message = MIMEMultipart()
    message["From"] = send_from
    message["To"] = send_to
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText("""A regarder""", "plain"))


    # Open PDF file in binary mode
    with open(file_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_path}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    return text


def send_email(file_path: str):
    smtp_server = os.environ.get("SMTP_SERVER")
    port = os.environ.get("SMTP_PORT")  # For starttls
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_MDP")
    receiver_email = os.environ.get("EMAIL_RECEIVER")

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password, initial_response_ok=True)
        server.sendmail(
            sender_email,
            receiver_email,
            create_message(
                sender_email,
                receiver_email,
                "ALERT - Detection Automatique de Personnes",
                file_path=file_path,
            ),
        )
