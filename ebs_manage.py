import boto3

# CONSTANTS
from env import *

# import SG manager
from sg import createSG, deleteSG

# import EBS Manager
from ebs import *

# import Key Manager
from kp import createKP, deleteKP

# import EC2 Manager
from manageEC2 import createEC2, selectInstanceTag, stopEC2, cleanEC2

# crear un Security Group
sgIds=createSG()
keyname=createKP()

instanceId=createEC2(Name, ImageId, InstanceType, keyname, sgIds)


# Crear un EBS
volId= createEBS(AZ[0], VOLUMETYPE, SIZE, Name)

instance=selectInstanceTag(Name)
instance.attach_volume(VolumeId=volId, Device='/dev/sdf') 

# wait for the user press a key
input("Press Enter to continue...")

# Detach EBS
instance.detach_volume(VolumeId=volId)

# wait for the user press a key
input("Press Enter to continue...")

# Stop EC2
stopEC2(instance.id)
deleteKP(
        KeyName='kp'+name,
    )
deleteSG(
    GroupId=sgIds,
)


# TODO: borrar el EBS
# deleteEBS(volId)

# Terminate EC2
# terminateEC2(instanceId)