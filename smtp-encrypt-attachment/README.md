# Virtru SDK Secure Email Attachment
Sends an unencrypted email with a Virtru Encrypted attachment


## Prerequisites
* [https://www.python.org/downloads/](Python 3)
* [https://docs.python.org/3/library/smtplib.html](Python3 SMTP Library)
* [https://developer.virtru.com/docs/getting-started-python](Virtru Python SDK)
* [https://support.google.com/a/answer/176600?hl=en](Gmail Relay)


## Update fields
* smtp_from_address
* smtp_to_address
* smtp_cc_address
* virtru_appid
* virtru_owner
* file_name_tdf
* file_path_plain
* file_path_tdf

## Usage
```
python3 app.py
```

## Virtru Authentictaion
Virtru authentication is managed using [https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded](App Ids)


## Demo
This will:
* Create a multipart MIME email
* Encrypt the file from the local file system
* Attach the encrypted file to the email
* Send the email
