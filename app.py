# dependency import 
from chalice import Chalice
import json

# importing the class from chalicelib
from chalicelib.sms import sms
from chalicelib.voice import voice
from chalicelib.slack_bot import slack_user
from chalicelib.whatsapp import whatsapp
from chalicelib.mongo_code.data.mongo_setup import global_init


# initialising the chalice app
app = Chalice(app_name='notifications')
app.debug = True

# def for generalising how and where do we want to send the message , the function takes the class and 
# the function name as input and executes the task. 
def channelise(info , event , channel):
    user1 = channel(data = info)
    channel.send_msg(user1)

# def for generalising the conditions applied
def conditions(channel_json , channel , event) :
    info = json.loads(event.message)
    if channel_json in info["channel"]: 
        channelise(info , event , channel)
        
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)



@app.on_sns_message(topic='notifications')
def Send_SMS(event):
    conditions(channel_json = "sms" , channel = sms , event = event)

@app.on_sns_message(topic='notifications')
def Send_Slack(event):
    conditions(channel_json = 'slack' , channel = slack_user , event = event)

@app.on_sns_message(topic='notifications')
def Send_voice(event):
    conditions(channel_json = 'voice' , channel = voice , event = event)
    
    


# # decorator for initialising the  Send_Voice lambda function with 'notifications' sns topic
# @app.on_sns_message(topic='notifications')
# # def for sending the message to user through voice call with conditions provided by trigger.json
# def Send_Voice(event):
#     conditions(channel_type = 'voice' , channel_class_name = voice , event = event)

# # decorator for initialising the  Send_slack lambda function with 'notifications' sns topic
# @app.on_sns_message(topic='notifications')
# #  def for sending the message to user through slack with conditions provided by trigger.json
# def Send_Slack(event):
#     conditions(channel_type = 'slack' , channel_class_name = slack_user , event = event)


# # decorator for initialising the  Send_whatsapp lambda function with 'notifications' sns topic
# @app.on_sns_message(topic='notifications')
# #  def for sending the message to user through whatsapp with conditions provided by trigger.json
# def Send_Whatsapp(event):
#     conditions(channel_type = 'whatsapp' , channel_class_name = whatsapp , event = event)












