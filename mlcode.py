import json
import boto3
import random

# Initialize the boto3 S3 client
s3_client = boto3.client('s3')

from datetime import datetime, timedelta

# Current date and time
now = datetime.now()

# Format the output
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
now = datetime.now() - timedelta(hours=5)
formatted_date2 = now.strftime("%Y-%m-%d %H")

print("Formatted date and time:", formatted_date2)

# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="gUDi89bLGcthuemUoJwV")
# project = rf.workspace("singapore-institute-of-technology-4vowg").project("people_detection-smfuq")
# version = project.version(4)
# dataset = version.download("tfrecord")

client = boto3.client('rekognition')

# Initialize a Boto3 client for DynamoDB
dynamodb = boto3.resource('dynamodb')

# Reference to your DynamoDB table
table = dynamodb.Table('Spaces_1')
table1 = dynamodb.Table('Spaces_graph')


def lambda_handler(event, context):
    bucket_name = 'awshtsl-newdataset'

    images_list = []

    # Example for populating the 'train_images' list
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            # Assuming you only want to add the file name, not the full path
            file_name = obj['Key'].split('/')[-1]
            images_list.append(file_name)

    # print(f"Collected {len(test_images)} 'test' images, {len(train_images)} 'train' images, and {len(valid_images)} 'valid' images.")

    # bucket_name = "myimagebucket1"
    file_name = images_list[1]

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket_name,
                                                        'Name': file_name}},
                                    MaxLabels=100,
                                    MinConfidence=70
                                    )
    # print(response)

    persons = [label for label in response['Labels'] if label['Name'] == 'Person']

    num_instances = 0
    # counter = 0
    if persons:
        for person in persons:
            # Check if there are instances detected
            if 'Instances' in person:
                num_instances = len(person['Instances'])  # Count the number of instances
                print(f"Person instances detected: {num_instances}")
    else:
        print("No 'Person' labels detected.")

    max = len(images_list)
    base_string = 'Floor'
    total_people = 0

    for i in range(5):
        floor = i + 1
        outputFloor = base_string + str(floor)
        ran = random.randint(0, max)
        file_name = images_list[ran]
        response = client.detect_labels(Image={'S3Object': {'Bucket': bucket_name,
                                                            'Name': file_name}},
                                        MaxLabels=100,
                                        MinConfidence=70
                                        )
        persons = [label for label in response['Labels'] if label['Name'] == 'Person']

        num_instances = 0
        # counter = 0
        if persons:
            for person in persons:
                # Check if there are instances detected
                if 'Instances' in person:
                    num_instances = len(person['Instances'])  # Count the number of instances
                    print(f"Person instances detected: {num_instances}")
        else:
            print("No 'Person' labels detected.")

        item = {
            'floor_name': outputFloor,  # Partition Key
            'num_people': num_instances,
            'date': formatted_date,

        }
        item1 = {
            'floor_name': outputFloor,  # Partition Key
            'date': formatted_date2,
            'num_people': num_instances,

        }
        total_people += num_instances
        response = table.put_item(Item=item)
        response = table1.put_item(Item=item1)

    # Example data to insert
    # Assuming floor_name is a string (e.g., 'Floor1') and num_people is an integer

    # Insert the item into the table
    item = {
        'floor_name': 'Total',  # Partition Key
        'num_people': total_people,
        'date': formatted_date,
    }
    response = table.put_item(Item=item)

