from chalicelib.slack_bot import slack_user
import json 

if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger.json').read())
    user1 = slack_user(data = info)
    user1.send_msg()    
