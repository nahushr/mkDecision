import json
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint
import boto3
import uuid


def lambda_handler(event, context):
    # TODO implement
    name = event["name"]
    destination_email = event["destinationEmail"]
    source_email = event["sourceEmail"]
    message_from_user = event["message"]
    subject = "Test email from ses using lambda"

    result, result_message = SMTP_Function(source_email, destination_email, message_from_user, name, subject)
    db_result_message = dynamodb_response = insert_data_in_dynamodb(name, source_email, destination_email,
                                                                    message_from_user)
    print(dynamodb_response)
    if (result == True):
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(result_message + ":::" + str(db_result_message))
        }

    return {
        'statusCode': 400,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(result_message + ":::" + str(db_result_message))
    }


def insert_data_in_dynamodb(name, source_email, destination_email, message, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('mkdecision')
    response = table.put_item(
        Item={
            'id': str(uuid.uuid1()),
            'name': name,
            'source_email': source_email,
            'destination_email': destination_email,
            'message': message
        }
    )
    return response


def SMTP_Function(source_email, destination_email, message_from_user, name, subject):
    SENDER = source_email
    SENDERNAME = name

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = destination_email

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIAQ6SLDTI367LKH3MB"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "BAWpRotEXOmXUqkvlygVFiN9t+MtfDZeV1rhUKeiV4en"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    # CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
    # endpoint in the appropriate region.
    HOST = "email-smtp.us-east-1.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <b>This email was sent with Amazon SES using the</b> <br>
      <p>Name:{}</p><br/>
      <p>Message: {}</p>
    </body>
    </html>
    """.format(name, message_from_user)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print("Error: ", e)
        return False, str(e)

    print("Email sent!")
    return True, "email sent successfully"
