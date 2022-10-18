import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from wsgiref.simple_server import server_version

class SMTPMailer:
    def __init__(self, server, port=465, password=None, use_ssl=True) -> None:
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.password = password
        self.attachment_paths = []

    def attach_file(self, filename):
        """"""
        self.attachment_paths.append(filename)

    def send_email(self, sender, recipients, subject, body, attachments=None):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipients
        message["Subject"] = subject
        if attachments is None:
            attachments = []
        
        # Add body to email
        message.attach(MIMEText(body, "plain"))

        for file_path in attachments: 
            with open(file_path, "rb") as attachment: 
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", 
                    f"attachment; filename= {file_path}",) 
                message.attach(part)

        text = message.as_string()
        
        if self.use_ssl:
            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                if self.password is not None:
                    server.login(sender, self.password)
                    server.sendmail(sender, recipients, text)
        
        else:
            with smtplib.SMTP(self.server, self.port) as server:
                server.sendmail(sender, recipients, text)

        
def main():

    debug_server = 'localhost'
    debug_port = 1025
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "my@gmail.com"
    receiver_email = "your@gmail.com"
    # password = input("Type your password and press enter:")

    smtp = SMTPMailer(debug_server, port=1025, use_ssl=False)
    smtp.attach_file('test.csv')
    smtp.send_email(sender_email, receiver_email, subject, body)

if __name__ == '__main__':
    main()
