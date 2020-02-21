from gcloud import storage
import json
import os
from virtru_tdf3_python import Client, Policy, EncryptFileParam, LogLevel, Protocol

virtru_creds = ".virtru"
gcp_creds = ".gcp"
bucket_name = ".bucket"


def get_virtru_credentials():
    virtru_credentials = None
    with open(virtru_creds, 'r') as JSON:
        virtru_credentials_json = json.load(JSON)
        virtru_credentials = virtru_credentials_json[0]
    return virtru_credentials


def get_bucket():
    with open(bucket_name, 'r') as JSON:
        bucket_name_json = json.load(JSON)
        bucket = bucket_name_json[0]["bucket"]
    return bucket


def get_virtru_client():
    virtru_credentials = get_virtru_credentials()
    client = Client(owner=virtru_credentials["virtru_owner"],
                    app_id=virtru_credentials["virtru_appid"])
    return client


def get_gcp_client():
    client = storage.Client.from_service_account_json(gcp_creds, 'project')
    return client


def virtru_encrypt(plain_file_name,
                   encrypted_file_name):
    param = EncryptFileParam(in_file_path=plain_file_name,
                             out_file_path=encrypted_file_name)
    client = get_virtru_client()
    client.set_protocol(Protocol.Html)
    policy_id = client.encrypt_file(encrypt_file_param=param)
    print("Policy ID: " + policy_id)
    return policy_id


def virtru_decrypt(encrypted_file_name,
                   decrypted_file_name):
    client = get_virtru_client()
    client.decrypt_file(in_file_path=encrypted_file_name,
                        out_file_path=decrypted_file_name)


def gcp_upload_file(source_file_name, target_file_name, is_virtru_encrypt=False):
    client = get_gcp_client()
    bucket = client.bucket(get_bucket())

    if is_virtru_encrypt:
        print("Encrypt File: " + source_file_name)
        virtru_encrypt(source_file_name, target_file_name)
        blob = bucket.blob(target_file_name)
        print("Upload File: " + target_file_name)
        blob.upload_from_filename(target_file_name)
    else:
        blob = bucket.blob(target_file_name)
        print("Upload File: " + source_file_name)
        blob.upload_from_filename(source_file_name)


def gcp_download_file(remote_file_name, local_file_name=''):
    client = get_gcp_client()
    bucket = client.get_bucket(get_bucket())

    blob = bucket.blob(remote_file_name)

    temp_file_name = local_file_name + ".temp"
    print("Download File: " + local_file_name)
    blob.download_to_filename(temp_file_name)

    try:
        virtru_decrypt(temp_file_name, local_file_name)
        os.remove(temp_file_name)

    except:
        print("Not a TDF: " + local_file_name)
        os.rename(temp_file_name, local_file_name)


def main():
    original_file_name = 'test.jpg'
    plain_file_name = 'plain-test.jpg'
    decrypted_file_name = 'decrypted-test.jpg'
    encrypted_file_name = 'test.jpg.tdf.html'

    gcp_upload_file(original_file_name, plain_file_name, False)
    gcp_upload_file(original_file_name, encrypted_file_name, True)
    gcp_download_file(plain_file_name, plain_file_name)
    gcp_download_file(encrypted_file_name, decrypted_file_name)


main()
