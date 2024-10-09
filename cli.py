import boto3
import os
import re
from dotenv import load_dotenv
import sys

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

# Upload a local file to the bucket
def upload_file(local_file_path, s3_file_name):
    try:
        s3.upload_file(local_file_path, bucket_name, f"{prefix}{s3_file_name}")
        print(
            f"File '{local_file_path}' uploaded as '{s3_file_name}' to bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error uploading file: {e}")

# List files matching a regex pattern
def filter_files(regex_pattern):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])]

    # Filter files using regex
    matching_files = [file for file in files if re.search(regex_pattern, file)]

    print("Filtered files: ", matching_files)

# Delete files matching a regex pattern
def delete_files(regex_pattern):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])]

    for file in files:
        if re.search(regex_pattern, file):
            try:
                s3.delete_object(Bucket=bucket_name, Key=file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting file: {file}, error: {e}")


if __name__ == "__main__":
    command = sys.argv[1]

    if command == 'list':
        list_files()
    elif command == 'upload':
        local_file_path = sys.argv[2]
        s3_file_name = sys.argv[3]
        upload_file(local_file_path, s3_file_name)
    elif command == 'filter':
        regex_pattern = sys.argv[2]
        filter_files(regex_pattern)
    elif command == 'delete':
        regex_pattern = sys.argv[2]
        delete_files(regex_pattern)
    else:
        print("Error: Invalid command. Supported commands are 'list', 'upload', 'filter', and 'delete'.")
