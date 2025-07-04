import boto3
import os
from functools import lru_cache
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError


@lru_cache()
def get_ssm_param(name, default=None, with_decryption=True):
    """
    Fetch a parameter from AWS SSM Parameter Store.
    If unavailable (e.g., local), fallback to environment variable.
    """

    env_fallback_key = name.strip("/").replace("-", "_").replace("/", "_").upper()

    try:
        ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "ap-south-1"))
        response = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
        return response['Parameter']['Value']
    except (ssm.exceptions.ParameterNotFound, ClientError, NoCredentialsError, EndpointConnectionError):
        env_value = os.getenv(env_fallback_key, default)
        if env_value is not None:
            return env_value
        raise Exception(f"Missing required parameter: {name} and no fallback environment variable '{env_fallback_key}' found.")

