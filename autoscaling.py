import boto3

from lb import elb_manager
from sg import sg_manager
from kp import keypair_manager

# CONST
from env import *

def autoscaling():

    # create Security Groupo
    sgId=sg_manager()
    input("Creado SG")
    KeyName=keypair_manager()
    input("Creado KeyPair")
    elb_manager(sgId)
    input("Creado LB")
    
    
    ec2=boto3.resource('ec2')
    # Esta query está bien para obtener el listado de instancias corriendo
    # La utilizón en la clase para demostrar que no había ninguna antes de crear el launch Configuration
    # TODO: Limitar el alacance: 
    #       Esto obtiene todas las instancias corriendo, incluso las no relacionadas con este prj
    # instances=ec2.instances.filter(
    #     Filters=[{
    #         'Name':'instance-state-name',
    #         'Values': ['running']
    #     }]
    # )

    # for instance in instances:
    #     print (instance.id, instance.state)

    # Create teh Launch Configuration



    asclient=boto3.client('autoscaling')
    res=asclient.create_launch_configuration(
        LaunchConfigurationName='lc'+Name,
        ImageId=ImageId,
        KeyName=KeyName,
        SecurityGroups=sgId,
        InstanceType=InstanceType
    )

    input("Creado Launch Configuration")

    # Create the autoscaling Group 
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group
    res1=asclient.create_auto_scaling_group(
        AutoScalingGroupName='ag'+Name,
        LaunchConfigurationName='lc'+Name,
        MinSize=1,
        MaxSize=2,
        DesiredCapacity=1,
        LoadBalancerNames=['lb'+Name],
        AvailabilityZones=AZ
    )


    input("Presiona una tecla cuando quieras eliminar el grupo de auto esalado")

    res2=asclient.update_auto_scaling_group(
            AutoScalingGroupName='ag'+Name,
            LaunchConfigurationName='lc'+Name,
            MinSize=0,
            MaxSize=0,
            DesiredCapacity=0,
            # LoadBalancerNames=['lb'+Name], Solo para la creaction
            AvailabilityZones=AZ
        )