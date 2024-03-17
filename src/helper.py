import yaml
from time import time
from boto3 import Session
from botocore.client import ClientError
from datetime import datetime as dt

def parse_config(
        config_path: str
    ) -> dict:
    with open(config_path, "r") as config:
        try:
            return yaml.safe_load(config)
        except yaml.YAMLError as YAMLExc:
            raise YAMLExc
        except Exception as Exc:
            raise Exc

def get_ms() -> str: return str(round(time()*1000))
def get_dt() -> str: return f"{dt.now().year}{dt.now().month}{dt.now().day}"

# AWS helper functions:
def create_AWS_session(
        aws_access_key_id: str, 
        aws_secret_access_key: str
    ) -> Session:
    session = Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    return session

def create_S3_bucket(session: Session, bucket_name: str, bucket_location: str) -> None:
    s3 = session.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError:
        s3.create_bucket(Bucket=bucket_name, 
                         CreateBucketConfiguration={'LocationConstraint': bucket_location})
