~import json
import boto3
import base64

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:XXXX:breaking-news-topic"
sns = boto3.client("sns")

def lambda_handler(event, context):
    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"])
        news = json.loads(payload)

        print("Received News:", news)

        if news["priority"] == "HIGH":
            message = f"""
BREAKING NEWS 🚨

Headline: {news['headline']}
Source: {news['source']}
Time: {news['published_at']}
"""
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚨 Breaking News Alert",
                Message=message
            )
            print("Breaking news alert sent")

    return {"status": "processed"}