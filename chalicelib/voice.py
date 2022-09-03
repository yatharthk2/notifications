from twilio.rest import Client
import json
# import mongo_code
# from mongo_code.program_support import *
from chalicelib.mongo_code.program_support import *
# from mongo_code.data_service import *
from chalicelib.mongo_code.data_service import *
# from mongo_code.data.mongo_setup import global_init
from chalicelib.mongo_code.data.mongo_setup import global_init

class voice :
    def __init__(self , data ):
        self.error_flag = 0
        self.event = data
        if self.event['inreq'] == 'false':
            self.message = self.event["message"]
            self.UID = self.event["uid"]
            self.active_project = self.event["active_project"]
            self.activce_org = self.event["active_org_email"]
            self.channelID = self.event["channelid"]
            self.GID = self.event["gid"]
            self.Gname = self.event["groupname"]
        else :
            self.channelID = self.event["channelid"]
            self.message = self.event["message"]
            self.phone = self.event["phone"]
        global_init()


    def fetch_info(self , uid) :
        
        self.user  = find_UID_in_project(self.active_project , uid)
        self.channel = fetch_channel(self.channelID)
        self.account  = self.channel.twiliosid
        self.token = self.channel.twiliotoken
        self.to_number = self.user.phonenum
        self.from_ = self.channel.twilio_number 
        self.client = Client(self.account, self.token)

    def fetch_info_ir(self ):
        self.channel = fetch_channel(self.channelID)
        self.account  = self.channel.twiliosid
        self.token = self.channel.twiliotoken
        self.to_number = self.phone
        self.from_ = self.channel.twilio_number 
        self.client = Client(self.account, self.token)    
        
            
    def format_outline(self ) :
        self.fetch_info(self.UID)
        try:
            phone_number = self.client.lookups.v1.phone_numbers(self.to_number).fetch()
            error_flag = 0
            print('number succesfully verified ')
        except Exception as e:
            error_flag = 1
        if error_flag == 0:
            try:
                call = self.client.calls.create(twiml='<Response><Say>' + self.message + '</Say></Response>',
                                   to=self.to_number,
                                   from_=self.from_,
                                   )
            except Exception as e:
                print("Valid Format but Number Not Found")
        else:
            print('Invalid Format and number not found')

    def format_outline_GID (self) :
        group = get_GID_information(self.Gname , self.active_project)
        for uid in group.uid:
            print(uid)
            self.fetch_info(uid) 
            try:
                call = self.client.calls.create(twiml='<Response><Say>' + self.message + '</Say></Response>',
                                   to=self.to_number,
                                   from_=self.from_,
                                   )
            except Exception as e:
                print("Valid Format but Number Not Found")

    def format_outline_ir(self ) :
        self.fetch_info_ir()
        try:
            phone_number = self.client.lookups.v1.phone_numbers(self.to_number).fetch()
            error_flag = 0
            print('number succesfully verified ')
        except Exception as e:
            error_flag = 1
        if error_flag == 0:
            try:
                call = self.client.calls.create(twiml='<Response><Say>' + self.message + '</Say></Response>',
                                   to=self.to_number,
                                   from_=self.from_,
                                   )
            except Exception as e:
                print("Valid Format but Number Not Found")
        else:
            print('Invalid Format and number not found')
    

    def send_msg(self):
        if self.event['inreq'] == 'false':
        
            if self.GID != 'None':
                print('gid found')
                self.format_outline_GID()
            if self.UID != 'None':
                print('uid found 1')
                self.format_outline()
        
        if(self.event['inreq'] == 'true'): 
            self.format_outline_ir()

# for testing the functionality of code without deploying to the server
if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger.json').read())
    user1 = voice(data = info)
    user1.send_msg()


    


            




