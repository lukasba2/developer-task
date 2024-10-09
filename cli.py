import boto3
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

s3 = boto3.client('s3')

bucket_name = 'developer-task'
prefix = 'x-wing/'

# List files in the bucket
def list_files():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])]
    print("List of files: ", files)
    

import sys

if __name__ == "__main__":
    command = sys.argv[1]

    if command == 'list':
        list_files()
