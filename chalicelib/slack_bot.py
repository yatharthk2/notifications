import slack
from slack_sdk import WebClient
from chalicelib.mongo_code.program_support import *
from chalicelib.mongo_code.data_service import *
from chalicelib.mongo_code.data.mongo_setup import global_init
class slack_user :
    def __init__(self , data ):
        self.error_flag = 0
        self.event = data
        if self.event['inreq'] == 'false':
            # trigger_neo
            self.message = self.event["message"]
            self.UID = self.event["uid"]
            self.active_project = self.event["active_project"]
            self.channelID = self.event["channelid"]
            self.GID = self.event["gid"]
            self.Gname = self.event["groupname"]
            global_init()
        
        else :
            self.channelID = self.event["channelid"]
            self.message = self.event["message"]
            self.slack = self.event["slack"]
            global_init()

    def fetch_info(self , uid) :
        # mongo document user
        self.user  = find_UID_in_project(self.active_project , uid)
        self.channel = fetch_channel(self.channelID)

        self.SLACK_TOKEN = self.channel.slack_api_key
        self.slackID = self.user.slackid
        self.client = WebClient(token=self.SLACK_TOKEN)

    
    def fetch_info_ir(self ):
        self.channel = fetch_channel(self.channelID)
        self.SLACK_TOKEN = self.channel.slack_api_key
        self.slackID = self.slack
        self.client = WebClient(token=self.SLACK_TOKEN)

            
    def format_outline(self ) :
        self.fetch_info(self.UID)
        self.client.conversations_open(users=[self.slackID])
        self.client.chat_postMessage(channel=self.slackID, text=self.message , as_user=True)

    def format_outline_GID (self) :
        group = get_GID_information(self.Gname , self.active_project)
        for uid in group.uid:
            self.fetch_info(uid) 
            self.client.conversations_open(users=[self.slackID])
            self.client.chat_postMessage(channel=self.slackID, text=self.message , as_user=True)
    def format_outline_ir(self ) :
        self.fetch_info_ir()
        self.client.conversations_open(users=[self.slackID])
        self.client.chat_postMessage(channel=self.slackID, text=self.message , as_user=True)    
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
    user1 = slack_user(data = info)
    user1.send_msg()                




