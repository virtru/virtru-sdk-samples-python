# Virtru GCP
Example of how to Encrypt and Decrypt file into and out of Google Cloud Storage Buckets.  
[Related post](https://medium.com/virtru/secure-data-on-google-cloud-storage-c57bd432839a)

## Prerequisites
- [Virtru SDK](https://developer.virtru.com/docs/getting-started-python) - Allows Encryption/Decryption/Policy Management/Audit Record Access
- [Virtru Authentication Keys](https://developer.virtru.com/docs/how-to-add-authentication) - Virtru authentication  
- [Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets) - Will be the destination and source for encryption and decryption.
- [Google Cloud Service Account](https://console.cloud.google.com/apis/credentials/serviceaccountkey) - GCP authentication
- [Google Bucket Authentication](https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication) - With read and write access to the AWS Bucket
- [Google Cloud Storage Python SDK](https://cloud.google.com/storage/docs/reference/libraries) - Google Cloud Storage Python SDK Install Documentation

## Virtru Authentication
This example uses AppId authentication.  Credentials will be stored in the [.virtru](.virtru) file.    
Authentication Options:
- [AppId](https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded) - AppId Authentication allows encryption and decryption for the account owner of policies they own.
- [HMAC](https://developer.virtru.com/docs/how-to-add-authentication#section-2-hmac-token-and-secret) - HMAC allows encryption and decryption on behalf of all users in the organization.

## Google Cloud Authentication
This example uses a service account file that has been delegated read and write access to the bucket.  
[Instructions](https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication)

## Demo Actions:
* Upload a file `test.jpg` file to the bucket as `test.jpg`
* Upload and Encrypt a file `test.jpg` file to the bucket as `test.jpg.tdf3.html`
* Download the file as `test.jpg`
* Download and Decrypt the file as `decrypted_test.jpg`

```
# Clone the Repository
git clone git@github.com:virtru/virtru-sdk-python-samples.git

# Change Directory
cd virtru-sdk-python-samples/virtru-gcs

# Add Virtru HMAC Keys
# open .virtru 
# update "virtru_appid"
# update "virtru_owner"

# Add GCS Service Account
# open .gcp
# update with information the service account json 

# Add GCS Bucket Name
# open .bucket
# update "bucket" value

# Run Example
python3 virtru_gcs.py
```

## Example Output
```
Upload File: test.jpg
Encrypt File: test.jpg
Policy ID: 088b4fdd-dec2-400b-b9ea-a55fce84fa20
Upload File: test.jpg.tdf.html
Download File: plain-test.jpg
Not a TDF: plain-test.jpg
Download File: decrypted-test.jpg
```
