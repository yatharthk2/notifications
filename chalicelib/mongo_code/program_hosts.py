import datetime
from colorama import Fore
from dateutil import parser
from chalicelib.mongo_code.switchlang import switch
from chalicelib.mongo_code import state
import chalicelib.mongo_code.data_service as svc
import json


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('ca', create_account)
            s.case('p', register_project)
            s.case('l', log_into_account)
            s.case('lp', log_into_project)
            s.case("ch", channels)
            s.case("uc", update_channels)
            s.case('u' , users)
            s.case('du' , delete_user)
            s.case('uu' , update_user)
            s.case('g' , Gid_Register)
            s.case('gu' , Gid_Add_Uid)
            s.case('vu' , get_verify_user)
            s.case('vc' , get_verify_channel)
            s.case('vg' , get_verify_group)
            s.case('dg' , delete_group)
            s.case('ug' , update_group)
            s.case('dgu' , delete_group_user)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('-> New to open notif?')
    print('1) [C]reate an [a]ccount')
    print('2) [L]ogin to your account\n')
    print('-> Following actions Requires account login :')
    print('1) Register a new [P]roject')
    print('2) [L]ogin to a [p]roject')
    print('3) create [Ch]annels')
    print('4) [U]pdate [C]hannels \n')
    print('-> Following actions require project login :')
    print('1) register [U]sers')
    print('2) [U]pdate [U]sers')
    print('3) [D]elete [U]sers')
    print('4) register [G]roups')
    print('5) add [U]id to a [G]ID')
    print('6) [U]pdate [G]roups')
    print('7) [D]elete [G]roups')
    print('8) [D]elete [U]ser in [G]roups\n')
    print('-> Utilities :')
    print('1) [V]erify [U]sers')
    print('2) [V]erify [C]hannels')
    print('3) [V]erify [G]roups')



def create_account():
    print(' ****************** REGISTER **************** ')
    # input basic info
    name = input('What is your organisation name? ')
    email = input('What is your email? ').strip().lower()

    # check if account exists
    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with email {email} already exists.")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your email? ').strip().lower()
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in successfully.')

def register_project():
    print(' ****************** REGISTER PROJECT **************** ')

    if not state.active_account:
        error_msg('You must login to your org account to register a product.')
        return

    project_name = input('what is the name of your project? ')
    if not project_name:
        error_msg('Cancelled')
        return
    old_project = svc.find_project_by_name(project_name)
    if old_project:
        error_msg(f"ERROR: Project with name {project_name} already exists.")
        return
    project = svc.register_project(state.active_account , project_name = project_name)

    state.reload_project()
    success_msg(f'Registered new project with id {project.id}.')


def log_into_project():
    print(' ****************** LOGIN **************** ')

    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    project = input('Which project do you want to go to ?').strip().lower()
    account = svc.find_project_by_name(project)

    if not account:
        error_msg(f'Could not find project {project}.')
        return

    state.active_project = account
    success_msg('Logged in successfully.')

def get_verify_user():
    print(' ****************** Users **************** ')

    if not state.active_project:
        error_msg("You must mention a project to view users.")
        return
    uid = input('Enter the user id: ')
    lookup  = svc.find_UID_in_project(state.active_project.projectname , UID = uid)
    if lookup:
        for data in lookup:
            print(data , lookup[data])
    else:
        print("No user found")

def get_verify_channel():
    print(' ****************** CHANNELS **************** ')

    if not state.active_account:
        error_msg("You must mention a account to view channels.")
        return
    channelid = input('Enter the channel id: ')
    lookup  = svc.find_channel_in_owner(state.active_account , channelid)
    if lookup:
        # svc.get_channel_information(channel_id = channelid)
        for data in lookup:
            print(data , lookup[data])
    else:
        print("No channel found")

def get_verify_group():
    print(' ****************** Groups **************** ')

    if not state.active_project:
        error_msg("You must mention a project to view groups.")
        return
    groupid = input('Enter the group id: ')
    lookup  = svc.find_GID_in_project(state.active_project.projectname , groupid)
    if lookup:
        for data in lookup:
            print(data , lookup[data])
    else:
        print("No group found")

    
def channels():
    if not state.active_account:
        error_msg('You must login first to your org account to register channels')
        return
    # if not state.active_project:
    #     error_msg('You must login first to register a product.')
    #     return
    print(' ****************** CHANNELS **************** ')
    twiliosid = input('What is your twilio sid? ')
    twiliotoken = input('What is your twilio token? ')
    twilio_number = input('What is your twilio number for sending calls and voice mail? ')
    twilio_number_whatsapp = input('What is your twilio number for sending whatsapp messages? ')
    slack_api_key = input('What is your slack api key? ')
    teams_api_key = input('What is your teams api key? ')

    channel = svc.register_channels(state.active_account , twiliosid, twiliotoken, twilio_number,twilio_number_whatsapp, slack_api_key, teams_api_key)
    state.reload_account()
    success_msg(f'Registered new channel with id {channel.id}.')


def update_channels():
    if not state.active_account:
        error_msg('You must login first to your org account to update channels')
        return
    # if not state.active_project:
    #     error_msg('You must login first to register a product.')
    #     return
    print(' ****************** CHANNELS **************** ')
    channelid = input('Enter the channel id: ')
    twiliosid = input('What is your twilio sid? ')
    twiliotoken = input('What is your twilio token? ')
    twilio_number = input('What is your twilio number for sending calls and voice mail? ')
    twilio_number_whatsapp = input('What is your twilio number for sending whatsapp messages? ')
    slack_api_key = input('What is your slack api key? ')
    teams_api_key = input('What is your teams api key? ')

    channel = svc.update_channels_in_owner(state.active_account , channelid, twiliosid, twiliotoken, twilio_number,twilio_number_whatsapp, slack_api_key, teams_api_key)
    state.reload_account()
    success_msg(f'Updated channel with id {channel.id}.')



def users():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** USERS **************** ')
    json_path = input('Enter path to user json file: ')
    user_json = json.load(open(json_path))
    name = user_json['User']['name']
    email = user_json['User']['email']
    slackid = user_json['User']['slackid']
    teamsid = user_json['User']['teamsid']
    phonenum = user_json['User']['phonenum']
    whatsappnum = user_json['User']['whatsappnum']
    user = svc.register_users(state.active_account,state.active_project , name, email, phonenum, whatsappnum,  slackid, teamsid )
    state.reload_project()
    success_msg(f'Registered new user with id {user._id}.')

def delete_user():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** USERS **************** ')
    uid = input('Enter the user id: ')
    lookup  = svc.find_UID_in_project(state.active_project.projectname , UID = uid)
    if lookup:
        svc.delet_UID_in_project(state.active_project.projectname , uid)
        state.reload_project()
        success_msg(f'Deleted user with id {uid}.')
    else:
        print("User not found in project")

def update_user():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** USERS **************** ')
    uid = input('Enter the user id: ')
    lookup  = svc.find_UID_in_project(state.active_project.projectname , UID = uid)
    if lookup:
        name = input('Enter the name: ')
        email = input('Enter the email: ')
        slackid = input('Enter the slack id: ')
        teamsid = input('Enter the teams id: ')
        phonenum = input('Enter the phone number: ')
        whatsappnum = input('Enter the whatsapp number: ')
        svc.update_user_in_project(state.active_project.projectname , uid, name, email, slackid, teamsid, phonenum, whatsappnum)
        state.reload_project()
        success_msg(f'Updated user with id {uid}.')
    else:
        print("User not found in project")

def Gid_Register ():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** GID Register **************** ')
    GroupName = input('Enter the Group Name  ')
    gid = svc.register_GID(state.active_account,state.active_project , GroupName)
    state.reload_project()
    success_msg(f'Registered new user with id {gid._id}.')

def Gid_Add_Uid():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** GID Users **************** ')
    GroupName = input('Enter the Group Name  ')
    UserID = input('Enter the UID  ')
    gid = svc.add_UID_to_GID(state.active_account,state.active_project , GroupName, UserID)
    state.reload_project()
    success_msg(f'Registered new user to Group {gid.groupname}')


def delete_group():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** GROUPS **************** ')
    gid = input('Enter the group id: ')
    lookup  = svc.find_GID_in_project(state.active_project.projectname , GID = gid)
    if lookup:
        svc.delete_GID_in_project(state.active_project.projectname , gid)
        state.reload_project()
        success_msg(f'Deleted user with id {gid}.')
    else:
        print("User not found in project")

def update_group():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** GROUPS **************** ')
    gid = input('Enter the group id: ')
    lookup  = svc.find_GID_in_project(state.active_project.projectname , GID = gid)
    if lookup:
        GroupName = input('Enter the Group Name  ')
        svc.update_group_in_project(state.active_project.projectname , gid, GroupName)
        state.reload_project()
        success_msg(f'Updated user with id {gid}.')
    else:
        print("User not found in project")

def delete_group_user():
    if not state.active_account:
        error_msg('You must login first to register a product.')
        return
    if not state.active_project:
        error_msg('You must login first to register a product.')
        return
    print(' ****************** GROUPS **************** ')
    gid = input('Enter the group id: ')
    uid = input('Enter the user id: ')
    lookup  = svc.find_GID_in_project(state.active_project.projectname , GID = gid)
    if lookup:
        svc.delete_UID_in_GID(state.active_project.projectname , gid, uid)
        state.reload_project()
        success_msg(f'Deleted user with id {uid} from group {lookup.groupname}.')
    else:
        print("User not found in project")
    
def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.org_name}> '
        if state.active_project:
            text = f'{state.active_project.projectname}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
