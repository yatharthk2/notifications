from chalice import Chalice
from chalicelib.sms import sms
from chalicelib.voice import voice
from chalicelib.slack_bot import slack_user
from chalicelib.whatsapp import whatsapp
import json

app = Chalice(app_name='notifications')
app.debug = True

def channelise(info , event , channel , format):
    user1 = channel(data = info)
    format(user1)

@app.on_sns_message(topic='notifications')
def Send_SMS(event):
    info = json.loads(event.message)
    if info["channel"]["sms"] == "True":
        if info["format"]["remainder"] == "True":
            channelise(info , event , sms , sms.send_remainder)
        if info["format"]["availability"] == "True":
            channelise(info , event , sms , sms.send_availability)
        if info["format"]["doc_msg_remainder"] == "True":
            channelise(info , event , sms , sms.send_doc_msg_remainder)
        if info["format"]["appointment_confirmation"] == "True":
            channelise(info , event , sms , sms.send_appointment_confirmation)
        if info["format"]["change_in_appointment"] == "True":
            channelise(info , event , sms , sms.send_change_in_appointment)
        else :
            print("No SMS Format Selected")
    
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

@app.on_sns_message(topic='notifications')
def Send_Voice(event):
    info = json.loads(event.message)
    if info["channel"]["voice"] == "True":
        if info["format"]["remainder"] == "True":
            channelise(info , event , voice , voice.send_remainder)
        if info["format"]["availability"] == "True":
            channelise(info , event , voice , voice.send_availability)
        if info["format"]["doc_msg_remainder"] == "True":
            channelise(info , event , voice , voice.send_doc_msg_remainder)
        if info["format"]["appointment_confirmation"] == "True":
            channelise(info , event , voice , voice.send_appointment_confirmation)
        if info["format"]["change_in_appointment"] == "True":
            channelise(info , event , voice , voice.send_change_in_appointment)
        else :
            print("No SMS Format Selected")
    
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)

@app.on_sns_message(topic='notifications')
def Send_Slack(event):
    info = json.loads(event.message)
    if info["channel"]["slack"] == "True":
        if info["format"]["remainder"] == "True":
            channelise(info , event , slack_user , slack_user.send_remainder)
        if info["format"]["availability"] == "True":
            channelise(info , event , slack_user , slack_user.send_availability)
        if info["format"]["doc_msg_remainder"] == "True":
            channelise(info , event , slack_user , slack_user.send_doc_msg_remainder)
        if info["format"]["appointment_confirmation"] == "True":
            channelise(info , event , slack_user , slack_user.send_appointment_confirmation)
        if info["format"]["change_in_appointment"] == "True":
            channelise(info , event , slack_user , slack_user.send_change_in_appointment)
        else :
            print("No SMS Format Selected")
    
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)



@app.on_sns_message(topic='notifications')
def Send_Whatsapp(event):
    info = json.loads(event.message)
    if info["channel"]["whatsapp"] == "True":
        if info["format"]["remainder"] == "True":
            channelise(info , event , whatsapp , whatsapp.send_remainder)
        if info["format"]["availability"] == "True":
            channelise(info , event , whatsapp , whatsapp.send_availability)
        if info["format"]["doc_msg_remainder"] == "True":
            channelise(info , event , whatsapp , whatsapp.send_doc_msg_remainder)
        if info["format"]["appointment_confirmation"] == "True":
            channelise(info , event , whatsapp , whatsapp.send_appointment_confirmation)
        if info["format"]["change_in_appointment"] == "True":
            channelise(info , event , whatsapp , whatsapp.send_change_in_appointment)
        else :
            print("No SMS Format Selected")
    
    app.log.debug("Received message with subject: %s, message: %s",
                  event.subject, event.message)












