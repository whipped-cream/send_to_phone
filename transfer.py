#!/usr/bin/env python
import requests
import os
import argparse
import tarfile


def transfer(filename: str, instance: str) -> str:
    basename = os.path.basename(filename)
    filepath = os.path.abspath(filename)
    file = open(filepath, 'rb')

    upload_url = 'https://{0}/{1}'.format(instance, basename)

    try:
        response = requests.put(upload_url, file)
    except:
        print('Error: unable to transfer file')
        response = None  # Silence warning
        exit(1)

    return response.text


def archive(files: list) -> str:
    tarname = 'temp{0}.tar'.format(str(os.getpid()))
    cache_dir = os.environ.get('XDG_CACHE_HOME')
    if cache_dir is None:
        cache_dir = '.cache'
        os.mkdir(cache_dir)
    else:
        cache_dir += '/send_to_phone'
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    tarpath = '{0}/{1}'.format(cache_dir, tarname)
    with tarfile.open(tarpath, "w:gz") as tar:
        for file in files:
            filepath = os.path.abspath(file)
            basename = os.path.basename(file)
            tar.add(filepath, basename)

    return tarpath


def encrypt(file: str, key_path: str, ) -> str:
    print('TODO')
    return file
    # do something


def parse_args():
    parser = argparse.ArgumentParser(
        description='Utility to upload files to transfer.sh')
    parser.add_argument('files', nargs='+', help='Files to upload')
    parser.add_argument('-c', '--encrypt', action='store_true', help='Encrypt files before uploading', default=False)
    parser.add_argument('-z', '--compress', action='store_true',
                        help='Compress files before uploading. Automatically set if more than one filename is passed',
                        default=False)
    parser.add_argument('--instance', help='Instance to upload file to. Defaults to transfer.sh', default='transfer.sh')
    args = parser.parse_args()
    return args


def process_and_upload(files: list, encrypt_flag: bool = False, compress_flag: bool = False,
                       instance: str = 'transfer.sh') -> str:
    if len(files) > 1 or compress_flag:
        file = archive(files)
    else:
        file = files[0]

    if encrypt_flag:
        file = encrypt(file, 'password')

    download_url = transfer(file, instance)

    return download_url


if __name__ == "__main__":
    args = parse_args()

    download_url = process_and_upload(args)

    print(download_url)

    # test change
