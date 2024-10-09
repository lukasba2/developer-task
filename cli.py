import boto3
import os
import re
from dotenv import load_dotenv
import sys
import argparse

# Load environment variables
load_dotenv()

# Initialize S3 client with environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION', 'eu-central-1')  # Default to a specific region if not set

if not aws_access_key_id or not aws_secret_access_key:
    raise ValueError("AWS Access Key ID and Secret Access Key must be set in the .env file.")

s3 = boto3.client('s3', 
                  aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key, 
                  region_name=aws_region)

bucket_name = 'developer-task'
prefix = 'x-wing/'

def list_files() -> None:
    """List all files in the specified S3 bucket and prefix."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])] if 'Contents' in response else []
    
    if files:
        print("List of files: ", files)
    else:
        print("No files found in the bucket.")

def upload_file(file_path: str, s3_file_name: str) -> None:
    """Upload a local file to the specified location in the S3 bucket."""
    try:
        s3.upload_file(file_path, bucket_name, f"{prefix}{s3_file_name}")
        print(f"File '{file_path}' uploaded as '{s3_file_name}' to '{bucket_name}'.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
    except Exception as e:
        print(f"Error uploading file: {e}")

def filter_files(regex_pattern: str) -> None:
    """List files in the S3 bucket that match a given regex pattern."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])] if 'Contents' in response else []
    
    matching_files = [file for file in files if re.search(regex_pattern, file)]
    
    if matching_files:
        print("Filtered files: ", matching_files)
    else:
        print("No matching files found.")

def delete_files(regex_pattern: str) -> None:
    """Delete files in the S3 bucket that match a given regex pattern."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [content['Key'] for content in response.get('Contents', [])] if 'Contents' in response else []
    
    if not files:
        print("No files found to delete.")
        return

    for file in files:
        if re.search(regex_pattern, file):
            try:
                s3.delete_object(Bucket=bucket_name, Key=file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting file: {file}, error: {e}")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='CLI tool for managing S3 files.')
    parser.add_argument('command', choices=['list', 'upload', 'filter', 'delete'], help='Command to execute')
    parser.add_argument('args', nargs='*', help='Additional arguments for the command')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_files()
    elif args.command == 'upload' and len(args.args) == 2:
        upload_file(args.args[0], args.args[1])
    elif args.command == 'filter' and len(args.args) == 1:
        filter_files(args.args[0])
    elif args.command == 'delete' and len(args.args) == 1:
        delete_files(args.args[0])
    else:
        print("Error: Invalid arguments provided. Refer to the help message for correct usage.")
        parser.print_help()

if __name__ == "__main__":
    main()

