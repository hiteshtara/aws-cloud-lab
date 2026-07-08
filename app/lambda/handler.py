import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    item = {
        "id": "health",
        "message": "AWS Cloud Lab is running",
        "timestamp": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item)
    }
