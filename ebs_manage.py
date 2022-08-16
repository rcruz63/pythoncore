import boto3

# CONSTANTS
from env import *

# import SG manager
from sg import *

# import EBS Manager
from ebs import *

# import Key Manager
from key import *

# import EC2 Manager
from ec2 import *

# crear un Security Group
sgIds=sg_manager()
keyname=keypair_manager()

instanceId=createEC2(Name, ImageId, InstanceType, keyname, sgIds)


# Crear un EBS
volId= createEBS(AZ[0], VOLUMETYPE, SIZE)