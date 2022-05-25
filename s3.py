import random
import boto3

# CONST
from env import *

def s3_manager():

    # Create a Bucket
    s3client = boto3.client('s3')
    bucketname="{name}bucket{random:07d}".format(name=Name, random=random.randint(0, 999999))
    s3client.create_bucket(bucketname)

    # Put an Objet into the bucket 
    # TIP: Para crearlo open("hello.txt","w").write("Hello Dolly!")
    

    s3res=boto3.resource('s3')
    s3res.Object(bucketname,file).put(Body=open(file, 'rb'))

    print(s3client.get_object(
        Bucket=bucketname,
        key=file
    ))
    
    print(s3client.get_bucket_acl(
        Bucket=bucketname
    ))

    print(s3client.get_object_acl(
        Bucket=bucketname,
        Key=file
    ))

    buckets=s3res.buckets.all()
    for bucket in buckets:
        print(bucket.name)

    s3client.upload_file(file, bucketname, 'myfile.txt')

    s3client.download_file(bucketname, 'myfile.txt', 'newfile.txt')

    buckets=s3res.buckets.all()
    for bucket in buckets:
        for obj in bucket.objects.all():
            print(obj)

    s3client.delete_object(
        Bucket=bucketname,
        Key=file
    )

    buckets=s3res.buckets.all()
    for bucket in buckets:
        if (bucket.name == bucketname):
            for obj in bucket.objects.all():
                obj.delete()
            bucket.delete()
    
    buckets=s3res.buckets.all()
    for bucket in buckets:
        print(bucket.name)


s3_manager()

