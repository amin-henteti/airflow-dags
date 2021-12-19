# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 20:39:14 2021

@author: Henteti Amin
"""

import smtplib
import ssl
from email.mime.text import MIMEText


def send_msg(msg='message'):
    """send whats message

    Args:
        msg (str, optional): [description]. Defaults to 'message'.
    """
    import pywhatkit
    pywhatkit.sendwhatmsg('+330659943632', msg, 0, 2)


def sendEmail(objet='Subject', body_of_email='Hi'):
    receivers = ['aminhenteti21@gmail.com', ]
    username = 'maynouhenteti@yahoo.com'
    password = 'fxmsgdhjrykahwah'  # get the users password
    sender = username
    print(f'sending from {username}')
    msg = MIMEText(body_of_email)
    msg['Subject'] = objet
    msg['From'] = sender
    msg['To'] = ','.join(receivers) if type(receivers) == list else receivers

    # Connect to Gmail SMTP Server
    # Now that the message is complete, we must connect to the Gmail SMTP server.
    # In simpler terms, this will essentially log in to your Gmail account
    # so it can produce and send the message created from the last section.
    # We connect to the Gmail SMTP server with host 'smtp.gmail.com' and port 465.
    # Log in with your Gmail account details, and then the email with the message inside
    # will be sent off:
    s = smtplib.SMTP_SSL(host='smtp.mail.yahoo.com', port=465)
    print(objet)
    s.login(user=username, password=password)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

def sendEmail2_gmail(objet='Subject', body_of_email='Hi'):
    receivers = ['aminhenteti21@gmail.com', ]
    username = 'anonyme0000xx@gmail.com'
    password = 'anonyme0000@xx2'  # get the users password
    sender = username

    msg = MIMEText(body_of_email, 'html')
    msg['Subject'] = objet
    msg['From'] = sender
    msg['To'] = ','.join(receivers) if type(receivers) == list else receivers

    # Connect to Gmail SMTP Server
    # Now that the message is complete, we must connect to the Gmail SMTP server.
    # In simpler terms, this will essentially log in to your Gmail account
    # so it can produce and send the message created from the last section.
    # We connect to the Gmail SMTP server with host 'smtp.gmail.com' and port 465.
    # Log in with your Gmail account details, and then the email with the message inside
    # will be sent off:
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    print(objet)
    s.login(user=username, password=password)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

if __name__ == '__main__':
    sendEmail('aminhenteti21@gmail.com')
