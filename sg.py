import boto3

# CONST
from env import *

def createSG() -> list:
    
    conn = boto3.client('ec2')
    sg=conn.create_security_group(GroupName='sg'+Name, Description=Name + ':SG for ' + Name)

    # TODO: Que narices hace esto?? Porque no retorna el ID del SG??
    # Porque en muchas llamadas espera una lista
    groupid=sg['GroupId']
    groupIds=[]
    groupIds.append(groupid)
    return groupIds

def deleteSG(groupIds: list) -> None:
        
        conn = boto3.client('ec2')
        conn.delete_security_group(GroupId=groupIds[0])