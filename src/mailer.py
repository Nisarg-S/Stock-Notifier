import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from termcolor import colored

import os


class Mailer:

    def __init__(self, *args, **kwargs):
        self.sender = os.getenv('SENDER_EMAIL')
        self.password = os.getenv('SENDER_PASSWORD')
        self.receiver_email = os.getenv('RECIEVER_EMAIL')
        self.receiver_phone = os.getenv('RECIEVER_PHONE_MAILBOX')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.TLS_port = os.getenv('SMTP_PORT', 587)

    def send_message(self, message, body='''''', method='phone', *args, **kwargs) -> bool:
        if kwargs is not None:
            for key, value in kwargs.items():
                body += f'''{key} : {value} \n'''
        if args is not None:
            for arg in args:
                body += f'''{args} \n'''
        if method == 'phone':
            receiver = self.receiver_phone
        else:
            receiver = self.receiver_email

        for _ in range(3):
            try:
                session = smtplib.SMTP(self.smtp_server, self.TLS_port)
                session.starttls()
                session.login(self.sender, self.password)
                message.attach(MIMEText(body, 'plain'))
                session.sendmail(self.sender, receiver, message.as_string())
                session.quit()
                print(datetime.now(), colored("[SUCCESS] Mail sent.", 'green'))
                return True
            except Exception as e:
                print(datetime.now(), colored(
                    "[ERROR] Something went wrong when trying to reach the server.", 'red'), colored('Message :' + e, 'yellow'))

        print(datetime.now(), colored(
            "[ERROR] Number of trys exceeded, moving on to next request.", 'red'))
        return False

    def create_message_stock(self, stock='', alert_price='', curr_price='', method='phone', *args, **kwargs):

        message = MIMEMultipart()

        if method == 'phone':
            message['To'] = self.receiver_phone
        else:
            message['To'] = self.receiver_email

        message['From'] = self.sender
        message['Subject'] = f'{stock}'

        body = f'''{stock} is at ${curr_price}. ${round(alert_price - curr_price, 2)} below your watch price of ${alert_price}.'''

        return self.send_message(message, body, method, *args, **kwargs)

    def create_message_EOD(self, stocks=[], method='email', *args, **kwargs):
        message = MIMEMultipart()
        message['To'] = self.receiver_email
        message['From'] = self.sender
        message['Subject'] = 'Automated End of Day Stock Report'

        body = ''' Your stocks: \n\n'''

        for stock, price, alert_price in stocks:
            body += f'''{stock} closed at ${price}. Your alert price is ${alert_price} \n'''

        return self.send_message(message, body, method, *args, **kwargs)
