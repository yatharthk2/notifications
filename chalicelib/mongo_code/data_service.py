from typing import List, Optional
import datetime
import bson
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from data.owners import Owner
    from data.project_c import Project
    from data.user import User
    from data.channels import Channels
    from data.GID import Gid
else:
    # uses current package visibility
    from .data.owners import Owner
    from .data.project_c import Project
    from .data.user import User
    from .data.channels import Channels
    from .data.GID import Gid

def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.org_name = name
    owner.org_email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(org_email=email).first()
    return owner

def find_project_by_name(project_name: str) -> Project:
    project = Project.objects(projectname=project_name).first()
    return project



def find_UID_in_project(active_project: Project , UID) -> bool:
    
    project = find_project_by_name(active_project)
    try:
        user = project.User.filter(_id = UID).first()

    except Exception  as e:
        return None
    else:
        return user


    

def delet_UID_in_project(active_project: Project , UID):
    
    project = find_project_by_name(active_project)
    try:
        for user in project.User:
            if str(user._id) == UID:
                project.User.remove(user)
                project.save()
                return True
            else :
                return False

    except :
        print("user not deleted")
        return False
        


def find_channel_in_owner(active_organisation , channel_identity) -> bool:
    
    owner = find_account_by_email(active_organisation.org_email)
    try:
        Channel = Owner.objects(channel_id = channel_identity , org_name = active_organisation.org_name ).first()
    except:
        print ("no such channel found")
        return None
    
    else:
        print(f"channel id present in {owner.org_name}.")
        return Channel

def get_channel_information(channel_id) -> Channels:
    channel_info = Channels.objects(id = channel_id).first()
    for data in channel_info:
        print(data , channel_info[data])
        
def fetch_channel(channel_ID) -> Channels:
    
    channel= Channels.objects(id = channel_ID).first()
    return channel
    


# def get_user_information(uid , active_project: Project) -> User:
#     # user_info = User.objects(id = uid).first()
#     project = find_project_by_name(active_project)
#     user_info = project.User.filter(_id = uid).first()
#     return user_info

def get_GID_information(Gname , active_project: Project) -> Gid:
    # gid = Gid.objects(groupname = Gname).first()
    project = find_project_by_name(active_project)
    gid = project.Group.filter(groupname = Gname).first()
    return gid

def get_project_channels(channelID) -> Channels:
    channel_info = Channels.objects(id = channelID).first()
    return channel_info



    

def print_project_users(active_project: Project) -> List[User]:
    project = find_project_by_name(active_project.projectname)
    for user in project.user_id:
        print(user)
    
def register_project(active_account: Owner, project_name: str) -> Project:
    
    project = Project()
    project.projectname = project_name
    project.save()

    account = find_account_by_email(active_account.org_email)
    account.project_ids.append(project.id)
    account.save()

    return project

def register_channels(active_account: Owner, twiliosid, twiliotoken, twilio_number ,twilio_number_whatsapp , slack_api_key, teams_api_key) -> Channels:

    
    channels = Channels()
    channels.twiliosid = twiliosid
    channels.twiliotoken = twiliotoken
    channels.twilio_number = twilio_number
    channels.twilio_number_whatsapp = twilio_number_whatsapp
    channels.slack_api_key = slack_api_key
    channels.teams_api_key = teams_api_key
    channels.save()
    # project = find_project_by_name(active_project.projectname)
    # project.channel_id.append(channels.id)
    # project.save()
    owner = find_account_by_email(active_account.org_email)
    owner.channel_id.append(channels.id)
    owner.save()

    return channels

def update_channels_in_owner(active_account: Owner, channelid, twiliosid, twiliotoken, twilio_number ,twilio_number_whatsapp , slack_api_key, teams_api_key) -> Channels:
        
        channels = get_project_channels(channelid)
        channels.twiliosid = twiliosid
        channels.twiliotoken = twiliotoken
        channels.twilio_number = twilio_number
        channels.twilio_number_whatsapp = twilio_number_whatsapp
        channels.slack_api_key = slack_api_key
        channels.teams_api_key = teams_api_key
        channels.save()

        return channels

def register_users(active_account: Owner,active_project: Project , name, email, phonenum, whatsappnum,  slackid, teamsid ) -> User:
    

    users = User()
    users.username = name
    users.email = email
    users.phonenum = phonenum
    users.whatsappnum = whatsappnum
    users.slackid = slackid
    users.teamsid = teamsid
    
  
    project = find_project_by_name(active_project.projectname)
    project.User.append(users)
    project.save()
    return users

def register_GID(active_account: Owner,active_project: Project , GroupName):

    
    
    gid = Gid()
    gid.groupname = GroupName
    gid.user_id = None

  
    project = find_project_by_name(active_project.projectname)
    project.Group.append(gid)
    project.save()
    return gid

def add_UID_to_GID(active_account: Owner,active_project: Project , Gname, uid):
    
    project = find_project_by_name(active_project.projectname)
    gid = project.Group.filter(groupname = Gname).first()
    gid.uid.append(uid)
    
    project.save()
    return gid
    
def find_GID_in_project(active_project: Project , GID) -> bool:
    
    project = find_project_by_name(active_project)
    try:
        gid = project.Group.filter(_id = GID).first()
    except:
        print ("no such group found")
        return None
    
    else:
        return gid

def delete_GID_in_project(active_project: Project , GID):
    
    project = find_project_by_name(active_project)
    try:
        for group in project.Group:
            if str(group._id) == GID:
                project.Group.remove(group)
                project.save()
                return True
            else :
                return False
    except :
        print("group not deleted")
        return False


def delete_UID_in_GID(active_project: Project , GID, UID):
    
    project = find_project_by_name(active_project)
    try:
        for group in project.Group:
            if str(group._id) == GID:
                group.uid.remove(UID)
                project.save()
                return True
            else :
                return False
    except:
        print("user not deleted")
        return False


def update_user_in_project(active_project: Project , UID , name, email, phonenum, whatsappnum,  slackid, teamsid ) -> User:
    
    project = find_project_by_name(active_project)
    user = project.User.filter(_id = UID).first()
    user.username = name
    user.email = email
    user.phonenum = phonenum
    user.whatsappnum = whatsappnum
    user.slackid = slackid
    user.teamsid = teamsid
    project.save()
    return user

def update_group_in_project(active_project: Project , GID , GroupName) -> Gid:
    
    project = find_project_by_name(active_project)
    gid = project.Group.filter(_id = GID).first()
    gid.groupname = GroupName
    project.save()
    return gid




