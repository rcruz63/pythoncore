import boto3

#CONST
from env import *

def keypair_manager() -> str:

    conn = boto3.client('ec2')
    keypair=conn.create_key_pair(KeyName='kp'+Name)
    print (keypair['KeyMaterial'])

    with open('kp'+Name+".pem", "a") as f:
        chmod('kp'+Name+".pem", 0o0600)
        f.write(keypair['KeyMaterial'])
    
    return 'kp'+Name