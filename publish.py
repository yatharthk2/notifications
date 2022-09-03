
import boto3
import json
import argparse

import urllib

parser = argparse.ArgumentParser(description= 'make independent request to contact user')

parser.add_argument('--inreq', type=str, help='set permission to IndependentRequest' , default='false')
parser.add_argument('--channelid' , type=str, help='set channelid' , default='none')
parser.add_argument('--message', type=str, help='type message to be sent' , default='none')
parser.add_argument('--email', type=str, help='type email address to be sent' , default='none')
parser.add_argument('--slack' , type=str, help='type slack channel to be sent' , default='none')
parser.add_argument('--phone' , type=str, help='type phone number to be sent' , default='none')
parser.add_argument('--whatsapp_number' , type=str, help='type phone number to be sent' , default='none')
parser.add_argument('--contact', type = str , help ='add the channels through which you want to contact the person' , nargs='+')
args = parser.parse_args()

if args.inreq == 'false': 
    # reading the trigger.json file and converting it to a dictionary
    msg = json.loads(open('chalicelib/trigger_neo.json').read())

    # code to find notifications topi in sns topics to trigger it with the trigger.json file
    sns = boto3.client('sns')
    topic_arn = [t['TopicArn'] for t in sns.list_topics()['Topics']
                if t['TopicArn'].endswith(':notifications')][0]

    # code to publish the message to the topic             
    response = sns.publish(Message=json.dumps(msg),
                        Subject='notifications',
                        TopicArn=topic_arn,
                        )

    # for debugging purpose
    print(response['ResponseMetadata']['HTTPStatusCode'])

if args.inreq == 'true':
    msg = {
        'inreq': args.inreq,
        'channelid': args.channelid,
        'message': args.message,
        'email': args.email,
        'slack': args.slack,
        'phone': args.phone,
        'whatsapp_number': args.whatsapp_number ,
        'channel': args.contact

    }
    sns = boto3.client('sns')
    topic_arn = [t['TopicArn'] for t in sns.list_topics()['Topics']
                if t['TopicArn'].endswith(':notifications')][0]

    # code to publish the message to the topic             
    response = sns.publish(Message=json.dumps(msg),
                        Subject='notifications',
                        TopicArn=topic_arn,
                        )

    print(response['ResponseMetadata']['HTTPStatusCode'])
