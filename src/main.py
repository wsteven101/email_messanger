# email_messanger/src/main.py

import smtplib
from email_messenger import EmailMessenger


def main():
    sender_email = input("Enter your email: ")
    sender_password = input("Enter your password: ")
    recipient_email = input("Enter recipient email: ")

    smtp_server = "smtp.mailersend.net"
    smtp_port = 587

    table_data = {
        "UK": "67,000,000",
        "USA": "335,000,000",
        "Canada": "40,000,000",
        "Australia": "26,000,000"
    }
    total = sum(int(value.replace(",", "")) for value in table_data.values())

    # set to localhost for using the local default smtp
    if smtp_server == "localhost":
        email_messenger = EmailMessenger(sender_email, smtp_server="localhost", smtp_port=25)
    else:
        email_messenger = EmailMessenger(sender_email, sender_password, smtp_server=smtp_server, smtp_port=smtp_port)

    email_messenger.send_email(recipient_email, subject, total, table_data)
    
if __name__ == "__main__":
    main()