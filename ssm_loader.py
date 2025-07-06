# ssm_loader.py
import os
import boto3

def fetch_all_ssm_parameters(prefix="/python-demo/"):
    ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "ap-south-1"))

    next_token = None
    while True:
        kwargs = {
            "Path": prefix,
            "Recursive": True,
            "WithDecryption": True
        }
        if next_token:
            kwargs["NextToken"] = next_token

        response = ssm.get_parameters_by_path(**kwargs)

        for param in response.get("Parameters", []):
            key = param["Name"].replace(prefix, "").upper()
            os.environ[key] = param["Value"]

        next_token = response.get("NextToken")
        if not next_token:
            break
