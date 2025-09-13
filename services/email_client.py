import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def send_mail(mail:str,passwd:str,receiver:list[str]):
    logging.info("Sending emails ......")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = mail
    password = passwd

    sender_email = mail
    receiver_email = receiver
    print(receiver_email)
    subject = "Test Email from Python"
    body = "Hello! This is a test email sent from Python."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
    finally:
        server.quit()
