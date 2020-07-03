import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_results(source_file_name, target_file_name):

    # A wrapper for upload_file(). Using this because we may want to write to
    # separate subfolders in the bucket.
    # target_file_name can just be something like <<job_uuid>>.txt
    bucket = "raas-results"
    subfolder = "run_results"
    return upload_file(
        source_file_name, bucket, os.path.join(subfolder, target_file_name)
    )


def upload_file(source_file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param source_file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then source_file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use source_file_name
    if object_name is None:
        object_name = source_file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(source_file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    return True

def upload_string(job_id, string):
    bucket_name = "raas-results"
    subfolder = "run_results"
    
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, os.path.join(subfolder, "{}.json".format(job_id)))
    object.put(Body=string)