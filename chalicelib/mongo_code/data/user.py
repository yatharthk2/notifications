import mongoengine
# from chalicelib.mongo_code.data.GID import Gid
# from chalicelib.mongo_code.data.user import User
# from GID import Gid
# from user import User
from bson.objectid import ObjectId







class User(mongoengine.EmbeddedDocument):
    _id = mongoengine.ObjectIdField( required=True, default=ObjectId )
    username = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    slackid = mongoengine.StringField()
    teamsid = mongoengine.StringField()
    phonenum = mongoengine.StringField()
    whatsappnum = mongoengine.StringField()




    meta = {
        'db_alias': 'core',
        'collection': 'user'
    }
