import boto3

# CONST
from env import *

def wait4obj(bucket:str, objname:str) -> None:
    s3 = boto3.client('s3')

    s3_waiter = s3.get_waiter('object_exists')
    s3_waiter.wait(Bucket=bucket, Key=objname)
    for key in s3.list_objects_v2(Bucket=bucket)['Contents']:
        print('Key')
