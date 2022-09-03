from chalicelib.voice import voice
import json 

if __name__ == '__main__':
    info = json.loads(open('chalicelib/trigger.json').read())
    user1 = voice(data = info)
    user1.send_msg()    

# from chalicelib.mongo_code.data_service import *
# from chalicelib.mongo_code.data.GID import Gid
# from chalicelib.mongo_code.data.mongo_setup import global_init

# global_init()
# gid = Gid.objects(id = '6237a525b1853b2758d324ff')
