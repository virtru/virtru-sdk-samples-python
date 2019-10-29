# Virtru Boto3
Wrapper for [Boto3 AWS SDK for Python](https://github.com/boto/boto3) to allow Virtru encryption and decryption of files.  This allows developers to ensure all application data is secure in transit and at rest in S3.  This is particularly a problem when the developer does not control the S3 Bucket security.


## Prerequisites
- [Boto3](https://github.com/boto/boto3)
- [Virtru SDK](https://developer.virtru.com/docs/getting-started-python) - Allows Encryption/Decryption/Policy Management/Audit Record Access
- [Virtru Authentication Keys](https://developer.virtru.com/docs/how-to-add-authentication) - I have chosen to use HMAC authentication for this example.  The keys are in [.virtru](.virtru) file.
- [AWS Bucket](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) - Will be the destination and source for encryption and decryption.
- [AWS API Keys](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/) - With read and write access to the AWS Bucket

## Virtru Authentication
This example uses HMAC authentication.  Credentials will be stored in the [.virtru](.virtru) file.    
Authentication Options:
- [AppId](https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded) - AppId Authentication allows encryption and decryption for the account owner of policies they own.
- [HMAC](https://developer.virtru.com/docs/how-to-add-authentication#section-2-hmac-token-and-secret) - HMAC allows encryption and decryption on behalf of all users in the organization.

## S3 Authentictaion
This example uses the standard [S3 credential configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to access the credentials.  Optionally a helper method has been created.


## Demo
This will:
* Upload the `text.txt` file to an S3 Bucket named `uploadedfile_plain.txt` (Unencrypted)
* Download the `uploadedfile_plain.txt` from the S3 Bucket named `downloadedfile_plain.txt` (Unencrypted) 
* Upload the `text.txt` file to an S3 Bucket named `uploadedfile_tdf.txt.tdf` (Encrypted)
* Download the `uploadedfile_tdf.txt.tdf` from the S3 Bucket named `downloadedfile_tdf.txt` (Unencrypted)


```
# clone the repository
$ git clone git@github.com:virtru/virtru-sdk-python-samples.git

# change directory
$ cd virtru-sdk-python-samples/virtru-boto3

# add keys
# open .virtru 
# update "virtru_api_key"
# update "virtru_api_secret"

# Run Example
python3 virtru_boto3.py
```

## Add to project
### Include:
- .virtru
- virtru_boto3.py

### Replace existing boto3 calls: 
- `upload_file` =>  `virtru_upload_file` 
- `download_file` => `virtru_download_file`

### Encrypt and Upload
Additional Parameters
- `is_virtru_encrypt=True`
- `virtru_owner="user@domain.com"`

**boto3**
```
upload_file(local_file, bucket, s3_file)
```
**virtru-boto3**
```
virtru_upload_file(local_file, bucket, s3_file, is_virtru_encrypt=True, virtru_owner=virtru_owner)
```
### Decrypt and Download
Additional Parameters
- virtru_owner="user@domain.com"

**boto3**
```
download_file(bucket, s3_file, local_file)

```
**virtru-boto**
```
virtru_download_file(bucket, s3_file, local_file, virtru_owner)
```
