import datetime
from colorama import Fore
from dateutil import parser
# from switchlang import switch
# import state
# import data_service as svc
import json

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from switchlang import switch
    import state
    import data_service as svc
else:
    # uses current package visibility
    from .switchlang import switch
    from . import state
    from . import data_service as svc


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


def log_into_project(projectname):

    project = svc.find_project_by_name(projectname)

    if not project:
        error_msg(f'Could not find project {project}.')
        return
    else :
        print(project.projectname)

    state.active_project = project
    success_msg('Logged in successfully.')

def get_verify_user(uid , projectname):
    log_into_project(projectname)
    if not state.active_project:
        error_msg("user verification failed due to invalid project")
        return

    lookup  = svc.find_UID_existance_in_project(state.active_project.projectname , UID = uid)
    if lookup:
        user = svc.get_user_information(uid = uid)
        print('user verified successfully')
    else:
        user = None
        print('no such user exists')
    
def channels():
    if not state.active_account:
        error_msg('You must login first to your org account to register channels')
        return
    print(' ****************** CHANNELS **************** ')
    twiliosid = input('What is your twilio sid? ')
    twiliotoken = input('What is your twilio token? ')
    twiliosender = input('What is your twilio sender? ')
    slack_api_key = input('What is your slack api key? ')
    teams_api_key = input('What is your teams slack key? ')

    channel = svc.register_channels(state.active_account , twiliosid, twiliotoken, twiliosender, slack_api_key, teams_api_key)
    state.reload_account()
    success_msg(f'Register new project with id {channel.id}.')


def get_info():
    svc.get_user_information('Yatharth' , '61e951b29cc76284ec92081f' )

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
    gid = user_json['User']['GID']
    name = user_json['User']['name']
    email = user_json['User']['email']
    slackid = user_json['User']['slackid']
    teamsid = user_json['User']['teamsid']
    phonenum = user_json['User']['phonenum']
    whatsappnum = user_json['User']['whatsappnum']
    user = svc.register_users(state.active_account,state.active_project , gid, name, email, phonenum, whatsappnum,  slackid, teamsid )
    state.reload_project()
    success_msg(f'Registered new user with id {user.id}.')



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
    svc.add_UID_to_GID(state.active_account,state.active_project , GroupName, UserID)
    state.reload_project()





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
