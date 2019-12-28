import argparse
import multiprocessing
import os
import time

from virtru_tdf3_python import Client, Policy, EncryptFileParam, Protocol


class VirtruParams:
    def __init__(self, source_file, target_file, owner, token_key, token_secret, add_user):
        self.source_file = source_file
        self.target_file = target_file
        self.owner = owner
        self.token_key = token_key
        self.token_secret = token_secret
        self.add_user = add_user


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
    parser.add_argument("--concurrency", default=1, type=str, help="Maximum number of processes to use.")

    args = parser.parse_args()

    if args.action == "encrypt":
        print("Encrypting")
        encrypt_folder(args.source, args.target, args.owner, args.token_key, args.token_secret, args.add_user,
                       args.concurrency)
    else:
        print("Decrypting")
        decrypt_folder(args.source, args.target, args.owner, args.token_key, args.token_secret, args.concurrency)


def decrypt_folder(source_dir, target_dir, owner, token_key, token_secret, concurrency):
    p = multiprocessing.Pool(concurrency)
    files = os.listdir(source_dir)
    arr = []
    for file in files:
        if os.path.isfile(os.path.join(source_dir, file)):
            decrypt_params = VirtruParams(
                os.path.join(source_dir, file),
                os.path.join(target_dir, remove_extension(file)),
                owner,
                token_key,
                token_secret,
                ""
            )
            arr.append(decrypt_params)
    p.map(decrypt_file, arr)


def decrypt_file(decrypt_params):
    print("Source - {} Target - {}".format(decrypt_params.source_file, decrypt_params.target_file))
    client = Client(owner=decrypt_params.owner,
                    api_key=decrypt_params.token_key,
                    secret=decrypt_params.token_secret)

    uuid = client.decrypt_file(in_file_path=decrypt_params.source_file,
                               out_file_path=decrypt_params.target_file)
    print("Decrypt - Process ID: {}".format(os.getpid()))
    return uuid


def remove_extension(filename):
    newfilename = filename
    if newfilename.split(".")[-1].lower() == "html":
        newfilename = newfilename.strip(".html")
    if newfilename.split(".")[-1].lower() == "tdf3":
        newfilename = newfilename.strip(".tdf3")
    return newfilename


def encrypt_folder(source_dir, target_dir, owner, token_key, token_secret, add_user, concurrency):
    p = multiprocessing.Pool(int(concurrency))
    files = os.listdir(source_dir)
    arr = []
    for file in files:
        if os.path.isfile(os.path.join(source_dir, file)):
            encrypt_params = VirtruParams(
                os.path.join(source_dir, file),
                os.path.join(target_dir, file) + ".tdf3",
                owner,
                token_key,
                token_secret,
                add_user
            )
            arr.append(encrypt_params)
    p.map(encrypt_file, arr)


def encrypt_file(encrypt_params):
    print("Source - {} Target - {}".format(encrypt_params.source_file, encrypt_params.target_file))
    client = Client(owner=encrypt_params.owner,
                    api_key=encrypt_params.token_key,
                    secret=encrypt_params.token_secret)
    policy = Policy()
    policy.share_with_users([encrypt_params.add_user])

    param = EncryptFileParam(in_file_path=encrypt_params.source_file,
                             out_file_path=encrypt_params.target_file)
    param.set_policy(policy)
    client.set_protocol(Protocol.Zip)
    uuid = client.encrypt_file(encrypt_file_param=param)
    print("Encrypt - Process ID: {}".format(os.getpid()))
    return uuid


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
