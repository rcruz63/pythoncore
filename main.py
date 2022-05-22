from os import chmod, stat
import boto3
import sys
from whatIsMyIP import whatIsMyIP
from elb import elb_manager

# CONST
from env import *

# Creamos un Security Group
conn = boto3.client('ec2')

# TODO: hay que comprobar que no exista
sg=conn.create_security_group(GroupName='sg'+Name, Description='SG for Web')

groupid=sg['GroupId']
groupIds=[]
groupIds.append(groupid)

# print(groupid)
input("SG creado: %s" % groupid)

# Añadimos una regla que me permita conectarme desde mi IP por el puerto 22
# TODO: Eliminar reglas anteriores
try:
    ip = whatIsMyIP()
except:
    raise Exception("Falló la consulta ip")

input("Ip Publica: %s" % ip)

cidrip = ip + "/32" 

conn.authorize_security_group_ingress(GroupId=groupid, IpProtocol='tcp', CidrIp=cidrip,
    FromPort=22, ToPort=22)

# Creamos una SSH KEY y la salvamos a disco
# TODO: Hay que comprobar que no exista
keypair=conn.create_key_pair(KeyName='kp'+Name)
print (keypair['KeyMaterial'])

with open('kp'+Name+".pem", "a") as f:
    chmod('kp'+Name+".pem", 0o0600)
    f.write(keypair['KeyMaterial'])

input ("Hey SSH creada: kp"+Name+".pem")

# Creamos una instancia ec2
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(ImageId=ImageId, 
                                MinCount=1, 
                                MaxCount=1,
                                SecurityGroups=['sg'+Name],
                                KeyName='kp'+Name+".pem",
                                InstanceType=InstanceType)

# print(instance)
# TODO: terminar si falla

# TODO: Esperar a que esté corriendo
waiter = conn.get_waiter('instance_running')
ids = []
InstanceIds=[]
for i in instance:
    ids.append(i.id)
    # Para cada instancia se genera un diccionario para añadirlo al balanceador CLASSIC
    instId={'InstanceId':i.id}
    InstanceIds.append(instId)
waiter.wait(InstanceIds=ids)

# Listar las instancias que estan corriendo
id2s = []

# TODO: Este filtro se carga todas las instancias running, cuidado!!
instances=ec2.instances.filter(
    Filters=[{'Name':'instance-state-name','Values':['running']}])

for inst in instances:
    id2s.append(inst.id)
    print("ID: %s, Type: %s" %(inst.id, inst.instance_type))

## Añadir el balanceador

elb_manager(Name, InstanceIds, groupIds)

input ("Pulsa para parar las instancias")

# Se paran las instancias
ec2.instances.filter(InstanceIds=id2s).stop()

input("Pulsa para terminar las instancias")
# terminamos las instancias ¿y si quisieramos esperar a que estuvieran paradas?
# TODO: Chequear el estado de la instancia 
# TODO: conn.describe_instance_status(Filters=[{'Name':'','Values'} | InstanceIds ...])
ec2.instances.filter(InstanceIds=id2s).terminate()
conn.delete_key_pair(
    KeyName='kp'+Name,
)
waiter=conn.get_waiter('instance_terminated')
waiter.wait(InstanceIds=ids)
conn.delete_security_group(
    GroupId=groupid,
)
