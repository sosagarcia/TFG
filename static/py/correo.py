from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def sendEmail(msge, destinatario, asunto):
    # create message object instance
    msg = MIMEMultipart()
    message = msge
    # setup the parameters of the message
    password = "EmeyCe.123"
    msg['From'] = "monitycont@gmail.com"
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    return ("successfully sent email to %s:" % (msg['To']))
