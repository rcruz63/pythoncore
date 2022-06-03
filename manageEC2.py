import boto3

# CONST
from env import *

def createEC2(ami:str, instance_type:str, key_name:str, security_group_ids:list) -> str:
    ec2 = boto3.client('ec2')
    response = ec2.run_instances(
        ImageId=ami,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids
    )
    return response['Instances'][0]['InstanceId']

def deleteEC2(instance_id:str) -> None:
    ec2 = boto3.client('ec2')
    ec2.terminate_instances(InstanceIds=[instance_id])

def infoEC2(instance_id:str) -> dict:
    ec2 = boto3.client('ec2')
    return ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]

def listEC2() -> list:
    ec2 = boto3.client('ec2')
    return ec2.describe_instances()['Reservations']