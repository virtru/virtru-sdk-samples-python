# Virtru SDK Secure Email Attachment
Sends an unencrypted email with a Virtru Encrypted attachment


## Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [Python3 SMTP Library](https://docs.python.org/3/library/smtplib.html)
- [Virtru Python SDK](https://developer.virtru.com/docs/getting-started-python)
- [Gmail Relay](https://support.google.com/a/answer/176600?hl=en)


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
Virtru authentication is managed using [App Ids](https://developer.virtru.com/docs/how-to-add-authentication#section-1-appid-token-downloaded)


## Demo
This will:
* Create a multipart MIME email
* Encrypt the file from the local file system
* Attach the encrypted file to the email
* Send the email
