import mongoengine
if __package__ is None or __package__ == '':
    from GID import Gid
    from user import user
else:
    # uses current package visibility
    from .GID import Gid
    from .user import User

class Project(mongoengine.Document):
    
    projectname = mongoengine.StringField()
    # user_id = mongoengine.ListField(mongoengine.ReferenceField('User'))
    # group_id = mongoengine.ListField(mongoengine.ReferenceField('Gid'))
    Group = mongoengine.EmbeddedDocumentListField(Gid)
    User = mongoengine.EmbeddedDocumentListField(User)
    
    meta = {
        'db_alias': 'core',
        'collection': 'project'
    }
