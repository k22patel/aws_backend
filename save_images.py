import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ses_client = boto3.client('ses', region_name='us-east-1')  # Replace 'us-east-1' with your AWS region

    try:
        response = ses_client.send_email(
            Source='managementnaturaldisaster@gmail.com',  # Verified sender email address
            Destination={
                'ToAddresses': [
                    'managementnaturaldisaster@gmail.com'  # Verified recipient email address
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Test Email from AWS SES'
                },
                'Body': {
                    'Text': {
                        'Data': 'This is a test email sent from AWS SES using Lambda.'
                    }
                }
            }
        )
        print('Email sent! Message ID:', response['MessageId'])
        return {
            'statusCode': 200,
            'body': 'Email sent successfully.'
        }
    except ClientError as e:
        print('Email sending failed:', e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': 'Failed to send email.'
        }

