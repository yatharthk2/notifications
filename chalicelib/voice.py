import os
from decouple import config
from twilio.rest import Client
import json



class voice :
    def __init__(self , data ):
        self.account = config('TWILIO_ACCOUNT_sid')
        self.token = config('auth_token')
        self.client = Client(self.account, self.token)
        self.from_ = config('from_number')
        self.error_flag = 0
        self.event = data
        self.doctor = self.event["doctor_details"]["doctor_name"]
        self.patient = self.event["patient_details"]["patient_name"]
        self.to_number = self.event["patient_details"]["to_number"]
        self.date = self.event["appointment_details"]["date"]
        self.time = self.event["appointment_details"]["time"]
        self.doctor_avail = self.event["doctor_details"]["doctor_availability"]
        self.voice_msg = (f'hey {self.patient}  your appointment is scheduled with {self.doctor} for {self.date} at {self.time}')


    def format_outline(self , sentence) :
        try:
            phone_number = self.client.lookups.v1.phone_numbers(self.to_number).fetch()
            error_flag = 0
            print('number succesfully verified ')
        except Exception as e:
            error_flag = 1
        if error_flag == 0:
            try:
                call = self.client.calls.create(twiml='<Response><Say>' + sentence + '</Say></Response>',
                                   to=self.to_number,
                                   from_=self.from_,
                                   )
            except Exception as e:
                print("Valid Format but Number Not Found")
        else:
            print('Invalid Format and number not found')

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
    user1 = voice(data = info)
    user1.send_remainder()
    


            




