# ssm_loader.py
import boto3
import os
from functools import lru_cache

@lru_cache()
def get_ssm_param(name, default=None, with_decryption=True):
    ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "ap-south-1"))
    try:
        response = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
        return response['Parameter']['Value']
    except ssm.exceptions.ParameterNotFound:
        if default is not None:
            return default
        raise Exception(f"Missing required parameter: {name}")
