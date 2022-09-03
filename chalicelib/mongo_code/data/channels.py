import datetime
import mongoengine




class Channels(mongoengine.Document):
    twiliosid = mongoengine.StringField()
    twiliotoken = mongoengine.StringField()
    twilio_number = mongoengine.StringField()
    twilio_number_whatsapp = mongoengine.StringField()
    slack_api_key = mongoengine.StringField()
    teams_api_key = mongoengine.StringField()
    meta = {
        'db_alias': 'core',
        'collection': 'channels'
    }
