from datetime import datetime
import socket   # library to connect network
import json     
import ssl      #import Transport Layer Security
import boto3   #library for Simple Notification Service


def check_ssl_expiration(event, context):
    domain = event['queryStringParameters']['host'] #retrieve the domain name from the event object
    port = event.get('port', 443) #get the port
    sns_topic_arn = event['sns_topic_arn']

    # the above code will establish SSL connection in order to retrieve the certificate
    try:
        context = ssl.create_default_context() # create a default context
        s = context.wrap_socket(socket.socket(), server_hostname=domain)
        s.connect((domain, port))  # connect to the port and domain using the socket
        cert = s.getpeercert()       # retrieve certificate
        expiration_date = cert['notAfter']  #extract the expiration date 
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'error': str(e)})
        }