import random
import boto3

# CONST
from env import *

def s3_manager():

    # Create a Bucket
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    s3client = boto3.client('s3', region_name=region)
    # Tras el error: Regions outside of us-east-1 require the appropriate LocationConstraint 
    # to be specified in order to create the bucket in the desired region
    location = {'LocationConstraint': region}
    bucketname="{name}bucket{random:07d}".format(name=Name, random=random.randint(0, 999999))
    s3client.create_bucket(
        Bucket=bucketname,
        CreateBucketConfiguration=location
    )

    # Put an Objet into the bucket 
    # TIP: Para crearlo open("hello.txt","w").write("Hello Dolly!")
    

    s3res=boto3.resource('s3')
    s3res.Object(bucketname,file).put(Body=open(file, 'rb'))

    print(s3client.get_object(
        Bucket=bucketname,
        Key=file
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

    input("Pulsa para borrar")

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

