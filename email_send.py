import smtplib
import sys
import ssl
from email.message import EmailMessage


email_sender = 'cryptographyproject123@gmail.com'
email_password = 'itinobtdwqrsehwt'
email_receiver = sys.argv[1]
key = sys.argv[2]
subject = 'UNIQUE CODE'
body = f"""Hello,
Here is your unique token: ${key}
Thank you for using our service.
Best regards,
INDIAN GOVT"""
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())

print('Email Sent Successfully')