# boto3
import boto3

# CONST
from env import *

# Create EBS
# volId= createEBS(AZ[0], VOLUMETYPE, SIZE)
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_volume
# Client version
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_volume
def createEBS(AZ0, VolumeType, Size) -> str:
    ec2=boto3.resource('ec2')
    vol=ec2.create_volume(
        AvailabilityZone=AZ0,
        Size=Size,
        VolumeType=VolumeType
    )
    return vol.id


def listEBS() -> list:
    ec2=boto3.resource('ec2')
    vols=ec2.volumes.all()
    for vol in vols:
        print (vol.id, vol.state)
    return vols

def attachEBS(InstanceId):
    ec2=boto3.resource('ec2')
    vols=ec2.volumes.all()
    for vol in vols:
        print (vol.id, vol.state)
        if vol.state == 'available':
            ec2.Volume(vol.id).attach(
                InstanceId=InstanceId,
                Device='/dev/sdf'
            )

def detachEBS(InstanceId):
    ec2=boto3.resource('ec2')
    vols=ec2.volumes.all()
    for vol in vols:
        print (vol.id, vol.state)
        if vol.state == 'in-use':
            ec2.Volume(vol.id).detach(
                InstanceId=InstanceId,
                Device='/dev/sdf'
            )

def createSnapshot(VolumeId):
    ec2=boto3.resource('ec2')
    vol=ec2.Volume(VolumeId)
    snap=vol.create_snapshot(Description='Snapshot from '+VolumeId)
    return snap.id