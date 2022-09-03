import datetime
import mongoengine
# from data.project_c import Project

if __package__ is None or __package__ == '':
    # uses current directory visibility
    
    from data.project_c import Project
else:
    # uses current package visibility
    
    from ..data.project_c import Project

class Owner(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    org_name = mongoengine.StringField(required=True)
    org_email = mongoengine.StringField(required=True)
    project_ids = mongoengine.ListField()
    channel_id = mongoengine.ListField(mongoengine.ReferenceField('Channels'))

    meta = {
        'db_alias': 'core',
        'collection': 'owners'
    }
