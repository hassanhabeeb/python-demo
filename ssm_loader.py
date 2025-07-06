# ssm_loader.py
import boto3
import os

def fetch_all_ssm_parameters(prefix="/python-demo/"):
    region = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
    ssm = boto3.client("ssm", region_name=region)

    paginator = ssm.get_paginator('get_parameters_by_path')
    for page in paginator.paginate(Path=prefix, Recursive=True, WithDecryption=True):
        for param in page['Parameters']:
            key = param['Name'].split('/')[-1]
            value = param['Value']
            print(f'export {key}="{value}"')

if __name__ == "__main__":
    fetch_all_ssm_parameters()
