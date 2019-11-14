import argparse
import os
from virtru_tdf3_python import Client, Policy, EncryptFileParam, Protocol


def main():
    parser = argparse.ArgumentParser(description='Bulk Virtru SDK')
    parser.add_argument("--action",
                        choices=["encrypt", "decrypt"],
                        default=None, type=str, help="Action to perform on source files.")
    parser.add_argument("--source", default=None, type=str, help="Folder containing files to perform action against.")
    parser.add_argument("--target", default=None, type=str, help="Folder to output the files.")

    parser.add_argument("--owner", default=None, type=str, help="Owner of the Virtru policy.")
    parser.add_argument("--token_key", default=None, type=str, help="Virtru authorization key.")
    parser.add_argument("--token_secret", default=None, type=str, help="Virtru authorization secret.")
    parser.add_argument("--add_user", default=None, type=str, help="Add user to an encryption policy")

    args = parser.parse_args()

    if args.action == "encrypt":
        print("Encrypting")
        encrypt_folder(args.source, args.target, args.owner, args.token_key, args.token_secret, args.add_user)
    else:
        print("Decrypting")
        decrypt_folder(args.source, args.target, args.owner, args.token_key, args.token_secret)


def decrypt_folder(source_dir, target_dir, owner, token_key, token_secret):
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            decrypt_file(os.path.join(source_dir, file), os.path.join(target_dir, remove_extension(file)), owner,
                         token_key,
                         token_secret)


def decrypt_file(source_file, target_file, owner, token_key, token_secret):
    print("Source - {} Target - {}".format(source_file,target_file))
    client = Client(owner=owner,
                    api_key=token_key,
                    secret=token_secret)

    client.decrypt_file(in_file_path=source_file,
                        out_file_path=target_file)


def remove_extension(filename):
    newfilename = filename
    if newfilename.split(".")[-1].lower() == "html":
        newfilename = newfilename.strip(".html")
    if newfilename.split(".")[-1].lower() == "tdf3":
        newfilename = newfilename.strip(".tdf3")
    return newfilename


def encrypt_folder(source_dir, target_dir, owner, token_key, token_secret, add_user):
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            encrypt_file(os.path.join(source_dir, file), os.path.join(target_dir, file) + ".tdf3", owner, token_key,
                         token_secret, add_user)


def encrypt_file(source_file, target_file, owner, token_key, token_secret, add_user):
    print("Source - {} Target - {}".format(source_file,target_file))
    client = Client(owner=owner,
                    api_key=token_key,
                    secret=token_secret)
    policy = Policy()
    policy.share_with_users([add_user])

    param = EncryptFileParam(in_file_path=source_file,
                             out_file_path=target_file)
    param.set_policy(policy)
    client.set_protocol(Protocol.Zip)
    client.encrypt_file(encrypt_file_param=param)


if __name__ == '__main__':
    main()
