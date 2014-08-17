#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
import logging
import sys
import re

logging.basicConfig(filename='autoresponder.log',level=logging.DEBUG)


blacklist = ['linkedin.com', 'noreply', 'facebook.com', 'twitter.com']

if len(sys.argv) > 1 :
   mail = sys.argv[1]
else:
   mail = None
headers = None
if mail:
    send = True
    valid = True
    logging.debug('Inizio elaborazione nuovo messaggio...')
    if len(re.findall(r"[a-zA-Z0-9._]+\@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}", mail)) == 0:
        valid = False
        logging.debug('Indirizzo non valido')
    headers = Parser().parsestr(mail)
    fp = open("/path/to/email.txt/file", 'rb')

    msg = MIMEText(fp.read())
    fp.close()

    logging.debug('Oggetto messaggio di risposta: %s' % headers['subject'])
    msg['Subject'] = 'Subject: %s' % headers['subject']
    logging.debug('Destinatario nuovo messaggio di risposta: %s' % headers['from'])
    msg['To'] = headers['from']
    logging.debug('Mittente messaggio di risposta: %s' % headers['to'])
    msg['From'] = headers['to']
    for b in blacklist:
        if b in headers['from']:
            send = False
            logging.debug('Destinatario %s in blacklist' % headers['from'])
        else:
            logging.debug('Destinatario %s in whitelist' % headers['from'])

    s = smtplib.SMTP('localhost')
    if send and valid:
        s.sendmail(headers['to'], [headers['from']], msg.as_string())
        logging.debug('Messaggio inviato')
    else:
        logging.debug('Messaggio non inviato mittente in blacklist')
    s.quit()
logging.debug('Fine elaborazione messaggio...')
