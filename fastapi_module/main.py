# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI
import models
import boto3
import json 
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "welcome to open notif"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




@app.post('/publish')
async def publish(user_request: models.Publish):
    msg = {
    'inreq': models.Publish.inreq,
    'msg': models.Publish.msg,
    'uid': models.Publish.uid,
    'gid': models.Publish.gid,
    'groupname': models.Publish.groupname,
    'channelid': models.Publish.channelid,
    'active_project': models.Publish.active_project,
    'active_project_name': models.Publish.active_project_name,
    'channel': models.Publish.channel

    }
    print('success 1')
    sns = boto3.client('sns')
    topic_arn = [t['TopicArn'] for t in sns.list_topics()['Topics']
                if t['TopicArn'].endswith(':notifications')][0]
    print('success 2')
    # code to publish the message to the topic             
    response = sns.publish(Message=json.dumps(msg),
                        Subject='notifications',
                        TopicArn=topic_arn,
                        )
    print('success 3')

    return {'response': response['ResponseMetadata']['HTTPStatusCode']}


@app.post('/publish_ir', response_model=models.Response)
async def publish_ir(user_request: models.Publish_ir):
    msg = {
        'inreq': user_request.inreq,
        'channelid': user_request.channelid,
        'message': user_request.message,
        'email': user_request.email,
        'slack': user_request.slack,
        'phone': user_request.phone,
        'whatsapp_number': user_request.whatsapp_number ,
        'channel': user_request.channel

    }
    sns = boto3.client('sns')
    topic_arn = [t['TopicArn'] for t in sns.list_topics()['Topics']
                if t['TopicArn'].endswith(':notifications')][0]

    # code to publish the message to the topic             
    response = sns.publish(Message=json.dumps(msg),
                        Subject='notifications',
                        TopicArn=topic_arn,
                        )
    return {'response': response['ResponseMetadata']['HTTPStatusCode']}

