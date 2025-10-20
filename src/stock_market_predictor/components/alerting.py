import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

class Alerting:
    def __init__(self):
        load_dotenv()
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_password = os.getenv("EMAIL_PASSWORD")

    def send_email_alert(self, subject: str, body: str, to_email: str):
        if not self.sender_email or not self.sender_password:
            print("Email credentials not found. Skipping alert.")
            return

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = to_email

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"Alert email sent successfully to {to_email}")
        except Exception as e:
            print(f"Failed to send email alert. Error: {e}")
