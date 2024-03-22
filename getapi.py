import json
import boto3

dynamodb = boto3.resource('dynamodb')

# Reference to your DynamoDB table
table = dynamodb.Table('Spaces_1')

from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    response = table.scan()

    print(response)
    # Extract items from response
    items = response['Items']
    sorted_items = sorted(items, key=lambda x: x['floor_name'])
    # Return items in a format compatible with API Gateway
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(sorted_items, cls=DecimalEncoder)
    }


