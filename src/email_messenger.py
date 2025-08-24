import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailMessenger:
    
    @staticmethod
    def validate_email(email):
        """Validate email address format using a simple regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def __init__(self, sender_email, sender_password=None, smtp_server='localhost', smtp_port=25):
        if not self.validate_email(sender_email):
            raise ValueError(f"Invalid sender email address: {sender_email}")
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def build_html_table(self, table_data):
        html_table = """
        <table style="
            border: 4px solid lightgrey;
            border-collapse: collapse;
            margin-left: 4em;
            background-color: #e6f2ff;">
        """
        for key, value in table_data.items():
            html_table += (
                f"<tr>"
                f"<td style='border: 4px solid lightgrey; padding: 5px; background-color: #e6f2ff;'>{key}</td>"
                f"<td style='border: 4px solid lightgrey; padding: 5px; background-color: #e6f2ff;'>{value}</td>"
                f"</tr>"
            )
        html_table += "</table><br>"
        return html_table

    def build_email_body(self, total, table_data):
        html_table = self.build_html_table(table_data) if table_data else ""
        html_body = f"""
        <html>
          <body>
            <div style="font-family: Calibri, Arial, Helvetica, sans-serif; font-size: 16px;">
              To whom it may concern,<br><br>
              The total is <b>{total:,}</b><br><br>
              {html_table}
              <br><br>
              For more information please see 
              <a href="https://en.wikipedia.org/wiki/World_population" target="_blank">
                Wikipedia on World Populations
              </a>
              <br><br>
              Kind regards,<br>
              Mr. &amp; Mrs. World
            </div>
          </body>
        </html>
        """
        return html_body

    def create_message(self, recipient_email, subject, total, table_data):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = self.build_email_body(total, table_data)
        msg.attach(MIMEText(body, 'html'))

        return msg

    def send_email(self, recipient_email, subject, total, table_data):
        msg = self.create_message(recipient_email, subject, total, table_data)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Only use TLS and login if not using localhost
                if self.smtp_server != 'localhost' and self.sender_password:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")