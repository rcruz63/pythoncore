import boto3
from os import chmod, stat

#CONST
from env import *

def createKP() -> str:

    conn = boto3.client('ec2')
    key_name='kp'+Name

    keypair=conn.create_key_pair(KeyName=key_name)
    print (keypair['KeyMaterial'])

    with open(key_name+".pem", "a") as f:
        chmod(key_name+".pem", 0o0600)
        f.write(keypair['KeyMaterial'])
    
    return key_name

def deleteKP(key_name: str) -> None:

    conn = boto3.client('ec2')
    conn.delete_key_pair(KeyName=key_name)