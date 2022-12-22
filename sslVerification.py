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
        
#define time
    now = datetime.utcnow()  # current time
    expiration_date = datetime.strptime(expiration_date, '%b %d %H:%M:%S %Y %Z') # expiration date
    days_until_expiration = (expiration_date - now).days  # remaining date til expiration
    is_valid = now < expiration_daten # if the expiration date is greater that the current date, the certifate is valid
 
  # check expiration condition
    if not is_valid:    # if the certificate is note valid...
        sns = boto3.client('sns')
        try:
            sns.publish(TopicArn=sns_topic_arn, Message=f"SSL certificate for {domain} has expired") # send notifaction
        except Exception as e:  # if an error occurs
            
            return {
                'statusCode': 500,   # return internal server error
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({'error': str(e)})   # return the JSON version of the body
            }

    # create response
    response = {
        'domain_name': domain,
        'days_until_expiration': days_until_expiration,
        'is_valid': is_valid
    }
 #return response in JSON
    return {
        'statusCode': 200,      #indicate successful response
        'headers': { 'Content-Type': 'application/json' },
       'body': json.dumps(response)
       }

# In this function will call check_ssl_expiration with the event and context parsed.
def lambda_handler(event, context):
    response = check_ssl_expiration(event, context)
    return response
