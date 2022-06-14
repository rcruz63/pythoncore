import boto3

# CONST
from env import *


def createEC2(name:str, ami:str, instance_type:str, key_name:str, security_group_ids:list) -> str:
    ec2 = boto3.client('ec2')
    tags={'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': name}]}
    response = ec2.run_instances(
        ImageId=ami,
        name=name,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        TagSpecifications=tags
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

def stopEC2(instance_id:str) -> None:
    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=[instance_id])

def selectInstanceTag(tag:str):
    ec2 = boto3.resource('ec2')

    instances = ec2.instances.all()
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name' and tag['Value'] == tag:
                return instance

# Terminar una instancia
def stopEC2(instance_id:str) -> None:
    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=[instance_id])


def cleanEC2(name, Instance) -> None:
    ec2 = boto3.client('ec2')

    ec2.instances.filter(InstanceIds=Instance).terminate()
    
    waiter=ec2.get_waiter('instance_terminated')
    waiter.wait(InstanceIds=Instance)


