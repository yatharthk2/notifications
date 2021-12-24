import slack
import os
from decouple import config
import json
class slack_user :
    def __init__(self , data) :
        self.SLACK_TOKEN = config('SLACK_TOKEN')
        self.event = data
        self.doctor = self.event["doctor_details"]["doctor_name"]
        self.patient = self.event["patient_details"]["patient_name"]
        self.date = self.event["appointment_details"]["date"]
        self.time = self.event["appointment_details"]["time"]
        self.doctor_avail = self.event["doctor_details"]["doctor_availability"]
        
        self.client = slack.WebClient(token=self.SLACK_TOKEN)

    def format_outline(self , sentence) :
        self.text_msg = sentence
        self.client.conversations_open(users=["U02QGPKBTPU"])
        self.client.chat_postMessage(channel='U02QGPKBTPU', text=self.text_msg , as_user=True)

    def send_remainder(self ): 
        msg = f'Hi {self.patient} , your appointment is scheduled with {self.doctor} for {self.date} at {self.time}'
        self.format_outline(sentence = msg )

    def send_availability(self):
        msg = f'Hi {self.patient} , {self.doctor} is available on {self.doctor_avail}'
        self.format_outline(sentence = msg )
    

    def send_doc_msg_remainder(self):
        msg = f'Hi {self.patient} , {self.doctor} has sent you a message , pls check your profile'
        self.format_outline(sentence = msg )

    def send_appointment_confirmation(self):
        msg = f'Hi {self.patient} , we have confirmed your booking with {self.doctor} on {self.date} at {self.time}'
        self.format_outline(sentence = msg )

    def send_change_in_appointment(self):
        msg = f'Hi {self.patient} , we have changed your booking with {self.doctor} ,  updated details are {self.doctor} will consult you on {self.date} at {self.time}'
        self.format_outline(sentence = msg )



if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger.json').read())
    user1 = slack_user(data = info)
    user1.send_availability()    

