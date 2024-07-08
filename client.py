import smtplib
from email.mime.text import MIMEText

msg = MIMEText("This is a test email.")
msg['Subject'] = 'Test Email'
msg['From'] = 'sender@example.com'
msg['To'] = 'receiver@example.com'

with smtplib.SMTP('localhost', 8025) as server:
    # Initiate the SMTP conversation
    code, response = server.ehlo()
    print(f"EHLO response: {code}, {response}")

    # Specify the sender
    code, response = server.mail(msg['From'])
    print(f"MAIL FROM response: {code}, {response}")

    # Specify the recipient
    code, response = server.rcpt(msg['To'])
    print(f"RCPT TO response: {code}, {response}")

    # Send the email content
    code, response = server.data(msg.as_string())
    print(f"DATA response: {code}, {response}")