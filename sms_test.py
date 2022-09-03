from chalicelib.sms import sms
import json 

if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger.json').read())
    user1 = sms(data = info)
    user1.send_msg()    
