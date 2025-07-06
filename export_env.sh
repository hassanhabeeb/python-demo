#!/bin/bash

python3 <<EOF
import boto3
import os

ssm = boto3.client("ssm", region_name="ap-south-1")
prefix = "/python-demo/"
response = ssm.get_parameters_by_path(Path=prefix, Recursive=True, WithDecryption=True)
for param in response["Parameters"]:
    name = param["Name"].replace(prefix, "")
    value = param["Value"].replace('"', '\\"')
    print(f'export {name}="{value}"')
EOF

