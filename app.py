import json

from flask import Flask, request
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
import google.auth
import google.auth.transport.requests
import google.auth.transport.grpc
import google.auth.jwt
import googleapiclient.discovery

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
  # Extract the information from the Dialogflow request
  req = request.get_json(silent=True, force=True)
  information = req['queryResult']['parameters']

  # Set up the email transport using SMTP
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
  smtp_server.ehlo()
  smtp_server.starttls()
  smtp_server.login('your-gmail-address@gmail.com', 'your-gmail-password')

  # Set up the email options
  message = MIMEMultipart()
  message['to'] = 'destination-email-address@example.com'
  message['subject'] = 'Information from Dialogflow'
  message.attach(MIMEText(json.dumps(information)))

  # Send the email
  smtp_server.sendmail('your-gmail-address@gmail.com', 'destination-email-address@example.com', message.as_string())
  smtp_server.quit()

  # Return a success response to Dialogflow
  return json.dumps({
    'fulfillmentText': 'Email sent successfully'
  })

if __name__ == '__main__':
  app.run()
