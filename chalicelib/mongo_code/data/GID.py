import datetime
import mongoengine
from bson.objectid import ObjectId





class Gid(mongoengine.EmbeddedDocument):
    # twiliosid = mongoengine.StringField()
    # twiliotoken = mongoengine.StringField()
    # twilio_number = mongoengine.StringField()
    # twilio_number_whatsapp = mongoengine.StringField()
    # slack_api_key = mongoengine.StringField()
    # teams_api_key = mongoengine.StringField()
    # meta = {
    #     'db_alias': 'core',
    #     'collection': 'channels'
    # }
    _id = mongoengine.ObjectIdField( required=True, default=ObjectId )
    groupname = mongoengine.StringField()
    uid = mongoengine.ListField()
    meta = {
        'db_alias': 'core',
        'collection': 'gid'
    }
    