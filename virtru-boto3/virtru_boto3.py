import os
import json
import boto3
from virtru_tdf3_python import Client, Policy, EncryptFileParam, LogLevel, Protocol

def virtru_revoke(policyId, virtru_owner):
    """
    Allows revocation of a Virtru Policy ID.

    :param policyId: GUID representing the Policy ID of an encrypted File.
    :return: None
    """
    virtru_credentials = get_virtru_credentials()

    client = Client(owner=virtru_owner,
                    api_key=virtru_credentials["virtru_api_key"],
                    secret=virtru_credentials["virtru_api_secret"])
    client.revoke_policy(policyId)


def virtru_upload_file(filename, bucket, key,
                       callback=None, extra_args=None,
                       is_virtru_encrypt=False, virtru_owner=None):
    """
     Wrapper for the Boto3 AWS call "upload_file"
     AWS API credentials can be hardcoded if required

     Hardcoded Example:
       aws_credentials = get_aws_credentials()
       s3 = boto3.client(
          's3',
          aws_access_key_id=aws_credentials["aws_access_key_id"],
          aws_secret_access_key=aws_credentials["aws_secret_access_key"]
       )


     :param filename: Local filename of the object to upload
     :param bucket: Bucket is th name of the S3 bucket to which the file will be uploaded
     :param key: Name of the object when placed into the S3 bucket
     :param virtru_owner: Owner of the Virtru Decryption request
     :param extra_args: AWS S3 Optional arguments
     :param callback: AWS S3 Optional arguments
     :param is_virtru_encrypt: Flag that determines if a file will be encrypted
     :param virtru_owner: Required if the is_virtru_encrypt parameter
     :return: None
     """
    file_name_in = filename
    bucket_name = bucket

    s3 = boto3.client(
        's3'
    )

    if is_virtru_encrypt:
        virtru_encrypt(file_name_in, key, virtru_owner)
        s3.upload_file(key, bucket_name, key)revocation
    else:
        s3.upload_file(file_name_in, bucket_name, key)


def virtru_download_file(bucket, key, filename, virtru_owner,
                         extra_args=None, callback=None):
    """
    Wrapper for the Boto3 AWS call "download_file"
    AWS API credentials can be hardcoded if required

    Hardcoded Example:
      aws_credentials = get_aws_credentials()
      s3 = boto3.client(
         's3',
         aws_access_key_id=aws_credentials["aws_access_key_id"],
         aws_secret_access_key=aws_credentials["aws_secret_access_key"]
      )

    :param bucket: Bucket is th name of the S3 bucket from which the file(s) will be downloaded.
    :param key: Name of the object in the S3 bucket to download
    :param filename: Local filename of the object once downloaded
    :param virtru_owner: Owner of the Virtru Decryption request
    :param extra_args: AWS S3 Optional arguments
    :param callback: AWS S3 Optional arguments
    :return: None
    """
    s3 = boto3.client(
        's3'
    )

    temp_file_name = filename + ".temp"
    s3.download_file(bucket, key, temp_file_name)
    try:
        print("Attemping: " + temp_file_name + "  " + filename)
        virtru_decrypt(temp_file_name, filename, virtru_owner)

    except:
        pass
        print("Not a TDF: " + temp_file_name + "  " + key)
        print("Renaming: " + temp_file_name + "  " + filename)
        os.rename(temp_file_name, filename)


def virtru_encrypt(file_name_plain, file_name_tdf, virtru_owner):
    """
    Call to the Virtru SDK to encrypt a file.  This example used HMAC authentication.
    Authentication Options:
    - [AppId](https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded)
    - [HMAC](https://developer.virtru.com/docs/how-to-add-authentication#section-2-hmac-token-and-secret)

    :param file_name_plain: Filename of the input of the encryption process
    :param file_name_tdf: Filename of the output (TDF) of the encrypt
    :param virtru_owner: Owner of the Virtru Encryption policy
    :return:
    """
    virtru_credentials = get_virtru_credentials()

    client = Client(owner=virtru_owner,
                    api_key=virtru_credentials["virtru_api_key"],
                    secret=virtru_credentials["virtru_api_secret"])
    param = EncryptFileParam(in_file_path=file_name_plain,
                             out_file_path=file_name_tdf)
    client.set_protocol(Protocol.Zip)
    client.encrypt_file(encrypt_file_param=param)
    return file_name_tdf


def virtru_decrypt(file_name_tdf, file_name_plain, virtru_owner):
    """
    Call to the Virtru SDK to decrypt a file.  This example used HMAC authentication.
    Authentication Options:
    - [AppId](https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded)
    - [HMAC](https://developer.virtru.com/docs/how-to-add-authentication#section-2-hmac-token-and-secret)

    :param file_name_tdf: Filename of the TDF(TDF.HTML) to decrypt
    :param file_name_plain: Filename of the output of the decryption process
    :param virtru_owner: Requester of the decrypt call
    :return: None
    """
    virtru_credentials = get_virtru_credentials()

    client = Client(owner=virtru_owner,
                    api_key=virtru_credentials["virtru_api_key"],
                    secret=virtru_credentials["virtru_api_secret"])
    client.decrypt_file(in_file_path=file_name_tdf,
                        out_file_path=file_name_plain)


def get_virtru_credentials():
    """
    Return the Virtru HMAC Keys to encrypt or decrypt.  Can be used in place of the Virtru credentials file.

    Hardcoded Example:
    virtru_credentials = dict(virtru_api_key='<Virtru Provided>',
                          virtru_api_secret='<Virtru Provided>')
    :return:
    Dictionary containing the required HMAC Keys
    """
    virtru_credentials = None
    with open('.virtru', 'r') as JSON:
        virtru_credentials_json = json.load(JSON)
        virtru_credentials = virtru_credentials_json[0]

    return virtru_credentials


def get_aws_credentials():
    """
     Return the AWS API Keys to upload or download.  Can be used in place of the AWS credentials file.

     :return:
     Dictionary containing the required API Keys
     """
    aws_credentials = dict(aws_access_key_id='<AWS Credentials>',
                           aws_secret_access_key='<AWS Credentials>')
    return aws_credentials


def main():
    """
    Example usage of the Virtru Boto wrapper for S3 functionality.
    All files are reference from within the project.
    bucket_name: Bucket is th name of the S3 bucket to which the file(s) will be uploaded.
    file_name_in: Source file to upload/download and encrypt/decrypt.
    virtru_owner: Owner of the policy for encryption and requester for decryption.
    """
    bucket_name = "virtru-sdk-boto3"
    file_name_in = "test.txt"
    virtru_owner = "owner@domain.com"

    # Validate S3 Functionality
    # Uploads an unencrypted file
    # Downloads an unencrypted file
    virtru_upload_file(file_name_in, bucket_name, "uploadedfile_plain.txt")
    virtru_download_file(bucket_name, "uploadedfile_plain.txt", "downloadedfile_plain.txt", virtru_owner)

    # Validates Virtru Functionality
    # Virtru Encrypt file
    # Uploads the encrypted file
    # Downloads an encrypted file
    # Virtru Decrypt File
    virtru_upload_file(file_name_in, bucket_name, "uploadedfile_tdf.txt.tdf", is_virtru_encrypt=True,
                       virtru_owner=virtru_owner)
    virtru_download_file(bucket_name, "uploadedfile_tdf.txt.tdf", "downloadedfile_tdf.txt", virtru_owner)


main()
