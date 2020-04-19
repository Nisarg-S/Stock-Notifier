# Stock Notifier

This is a simple python program which allows you to recieve automated stock notifications when prices go above your watch price. A sample stock list can be found in the stocks.txt file, this is also what you an edit to add more stocks to your watchlist.

## How to set it up

This program is best run on a virtual server (i.e an EC2 server on AWS) as you ideally want to have this program running indefinitely. 

You will also need an email to sent the notfications from and either an email or phone number to recieve the notifications from. All these values are set as environment variables which you will need to provide values for after running the program for the first time. Here is a list of environment variables this program takes:

- SENDER_EMAIL
- SENDER_PASSWORD
- SMTP_SERVER
- SMTP_PORT
- RECIEVER_PASSWORD
- RECIEVER_PHONE_MAILBOX

After you have set up a virtual server, added the stocks you want to track to the stock.txt file and have these values you can enter the following into the console and you are good to go:

```console
pip install -r requirements.txt
python main.py
```