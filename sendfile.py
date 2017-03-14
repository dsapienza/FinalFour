import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from email import Encoders

def send_mail(send_from, send_to, subject, text, server="localhost"):
#def send_mail( files=[]):
#    assert type(send_to)==list
#    assert type(files)==list

#    send_from = 'dsapienza@gmail.com'
#    send_to   = 'benson22482@yahoo.com'
#    assert type(send_to)==list
#    subject   = 'Testing file attachement'
#    text      = 'Do you see me???'
    files     = ['finalfour.csv']
    assert type(files)==list
#    server    = 'localhost'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
      part = MIMEApplication(open(str(f),"rb").read())
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
      msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
