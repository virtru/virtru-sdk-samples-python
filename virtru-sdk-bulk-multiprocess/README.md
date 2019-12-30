# Virtru SDK Bulk Example
Tool to encrypt and decrypt files from a source folder to a target folder.

## Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [Virtru Python SDK](https://developer.virtru.com/docs/getting-started-python)


## Install Prerequisites
```
pip3 install argparse
```

## Required Parameters
* Action - Action to perform against source files
    * Encrypt
    * Decrypt
* Source - Directory of files to perform action against.
* Target - Directory to contain the files after action.
* Owner - Owner of the encryption policy
* Token Key - HMAC Token
* Token Secret - HMAC Secret
* Add User - Add user to encryption policy
* Concurrency - Maximum number of processes


## Virtru Authentictaion
Virtru authentication is managed using [HMAC Authentication](https://developer.virtru.com/docs/how-to-add-authentication#section-2-hmac-token-and-secret)


## Encrypt Example
```
python3 app.py --action encrypt \
--source "/tmp/source" \
--target "/tmp/target" \
--owner owner@domain.com \
--token_key P6EDZRUA7WCLLP73@tokens.virtru.com \
--token_secret n7U9kNHuWFvVKkD5 \
--add_user user@domain.com
--concurrency 5
```

## Decrypt Example
```
python3 app.py --action decrypt \
--source "/tmp/source" \
--target "/tmp/target" \
--owner owner@domain.com \
--token_key P6EDZRUA7WCLLP73@tokens.virtru.com \
--token_secret n7U9kNHuWFvVKkD5
--concurrency 5
```
