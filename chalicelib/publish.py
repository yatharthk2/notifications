
import boto3
import json

msg = json.loads(open('chalicelib/trigger.json').read())
sns = boto3.client('sns')
topic_arn = [t['TopicArn'] for t in sns.list_topics()['Topics']
             if t['TopicArn'].endswith(':notifications')][0]
response = sns.publish(Message=json.dumps(msg),
                       Subject='notifications',
                       TopicArn=topic_arn,
                       MessageAttributes= {
    "sms": {
        "DataType": "Number",
        "StringValue": "1"
    },
    "voice": {
        "DataType": "Number",
        "StringValue": "1"
    },
    "slack": {
        "DataType": "Number",
        "StringValue": "0"
    } ,
    "whatsapp": {
        "DataType": "Number",
        "StringValue": "0"
    }
})

print(response['ResponseMetadata']['HTTPStatusCode'])
