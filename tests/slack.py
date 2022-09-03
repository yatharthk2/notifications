from .. import chalicelib
import json 

if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger_neo.json').read())
    user1 = slack_user(data = info)
    user1.send_msg()    
