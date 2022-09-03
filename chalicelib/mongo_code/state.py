from typing import Optional

# from data.owners import Owner
# from data.project_c import Project
# import data_service as svc

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from data.owners import Owner
    import data_service as svc
    from data.project_c import Project
else:
    # uses current package visibility
    from .data.owners import Owner
    from . import data_service as svc
    from .data.project_c import Project

active_account: Optional[Owner] = None
active_project: Optional[Project] = None


def reload_account():
    global active_account
    if not active_account:
        return

    active_account = svc.find_account_by_email(active_account.org_email)


def reload_project():
    global active_project
    if not active_project:
        return

    active_project = svc.find_project_by_name(active_project.projectname)
