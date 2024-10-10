import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def sendmail(recipients_emails:list, title: str, content:str):
    """
    Функция отправки писем
    """
    smtp_server = "smtp.yandex.ru"


    login = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')


    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join(recipients_emails)

    s = smtplib.SMTP(smtp_server, 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], recipients_emails, msg.as_string())
    finally:
        # print(msg)
        s.quit()
