from pydantic import BaseModel


class Response(BaseModel):
    text: str
    


class Publish(BaseModel):
    inreq: str
    msg: str
    uid: str
    gid: str
    groupname: str
    channelid: str
    active_project: str
    active_project_name: str
    channel: list 

class Publish_ir(BaseModel):
    inreq: str
    message: str
    channelid: str
    phone: str
    email: str
    slack : str
    whatsapp_number : str 
    channel: list