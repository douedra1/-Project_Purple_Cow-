# -Project_Purple_Cow-
Fearless Site Reliability Engineer




I spent a lot of time trying to understand the requirements of my task. Once I understood what I was asked to do, I started brainstorming the potential solution.

Since I am checking the validation date of SSL certificates, I imported the Python library datetime. The response should be in JSON, so I also imported JSON as well as the SSL for the certificate and socket for the network communication. One of the requirements is to send a notification if the certification is not valid. To send the notification I imported boto3 which is the AWS library for sending notifications.

I established the connection using the hostname and the port number. Once the connection was established, I extracted the expiration date, and I compared it to the current time. If the expiration date is less than the current time, then a notification is sent, and I return the result in JSON format. I then created a function to test my SSL verification function on the same python file.

**List any future updates, changes, or outstanding code you would like to add or would recommend be added

It is not a good practice to let the certificate expires before the infrastructure trigger an alert. I will add another block of code to check if the certificate will expire in the next 15 days. If it is the case, the lambda function will be updated to notify the team so action can be taken as soon as possible.

The lambda function uses only SNS to send notification. I would update the code to add another method to send alerts when a certificate is about to expire. One other method that can be used is the SES (Simple Email Service)

The lambda function only checks the expiration date of the certificate. There are cases where a certificate has been revoked. It is important to also check that. To build this solution, I would update my code to check the information of the certification and verify if the information is up to date and still valid.

My code is designed to check only one domain at the time. It can be useful to make the code check multiple domains at the same. To do so, I would change my input type to make it an array that will contain multiple domains.

resource: https://registry.terraform.io/providers/hashicorp/aws/2.34.0/docs/guides/serverless-with-aws-lambda-and-api-gateway https://github.com/ilteriskeskin/ssl-check-api/blob/main/main.py https://aws.amazon.com/blogs/compute/implementing-mutual-tls-for-java-based-aws-lambda-functions/
