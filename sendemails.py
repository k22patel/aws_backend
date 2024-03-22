import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ses_client = boto3.client('ses', region_name='us-east-1')

    try:
        response = ses_client.send_email(
            Source='managementnaturaldisaster@gmail.com',
            Destination={
                'ToAddresses': [
                    'managementnaturaldisaster@gmail.com'
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Booking Space Notification!'
                },
                'Body': {
                    'Text': {
                        'Data': 'There is a Study Spot for you in Robarts! Please Check the Site for Details.Thank you & Goodluck Studying!'
                    }
                }
            }
        )
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return {'statusCode': 200, 'body': 'Email sent successfully'}
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': 'Error sending email'}

