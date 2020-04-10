import boto3
import sys
from carprice.exception import CarException
from carprice.logger import logging


def download_file_from_s3(bucket_name: str, object_key: str, local_file_path: str) -> None:
    """
    Downloads a file from an S3 bucket to a local directory.

    Args:
        bucket_name (str): Name of the S3 bucket.
        object_key (str): Key (path) of the object in the S3 bucket.
        local_file_path (str): Local path where the file will be saved.

    Raises:
        CarException: If an error occurs during the download process.
    """
    try:
        # Initialize the S3 client
        s3_client = boto3.client('s3')
        
        # Log the start of the download process
        logging.info(f"Initiating download from S3 bucket: {bucket_name}, Object Key: {object_key}")
        
        # Download the file from S3
        s3_client.download_file(bucket_name, object_key, local_file_path)
        
        # Log the successful completion of the download
        logging.info(f"File successfully downloaded from S3 bucket: {bucket_name} to {local_file_path}")
    
    except Exception as e:
        # Raise a custom exception with detailed error information
        logging.error(f"Error occurred while downloading file from S3: {e}")
        raise CarException(e, sys) from e