#!/usr/bin/env python
import requests
import os
from argparse import ArgumentParser
import zipfile
import platform
from halo import Halo


def transfer(filename: str, instance: str) -> str:
    basename = os.path.basename(filename)
    filepath = os.path.abspath(filename)
    file = open(filepath, 'rb')

    upload_url = 'https://{0}/{1}'.format(instance, basename)
    with Halo(text='Uploading files...', spinner='dots') as spinner:
        try:
            response = requests.put(upload_url, file)
            spinner.succeed('Done ')
        except:  # todo: handle errors individually
            print('Error: unable to transfer file')
            response = None  # Silence warning
            spinner.fail('💥💥💥💥Failed ')
            exit(1)

        return response.text


def archive(files: list) -> str:
    zipname = 'temp{0}.zip'.format(str(os.getpid()))
    cache_dir: str
    if platform.system() == 'Linux':
        cache_dir = os.environ.get('XDG_CACHE_HOME')
    elif platform.system() == 'Windows':
        cache_dir = os.environ.get('TEMP')
    else:
        cache_dir = None

    if cache_dir is None:
        cache_dir = os.path.expanduser('~')
        cache_dir = os.path.join(cache_dir, '.cache')

    cache_dir = os.path.join(cache_dir, 'send_to_phone')
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    with Halo(text='Uploading files...', spinner='dots') as spinner:
        zippath = os.path.join(cache_dir, zipname)
        with zipfile.ZipFile(zippath, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip:
            for file in files:
                filepath = os.path.abspath(file)
                basename = os.path.basename(file)
                zip.write(filepath, basename)
        spinner.succeed('Done ')

    return zippath


def encrypt(file: str, key_path: str, ) -> str:
    print('TODO')
    return file
    # todo


def parse_args():
    parser = ArgumentParser(
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
    compress_flag = len(files) > 1 or compress_flag
    if compress_flag:
        file = archive(files)
    else:
        file = files[0]

    if encrypt_flag:
        file = encrypt(file, 'password')

    download_url = transfer(file, instance)

    if compress_flag:
        os.remove(file)

    return download_url


if __name__ == "__main__":
    args = parse_args()

    download_url = process_and_upload(args.files, args.encrypt, args.compress)

    print(download_url)
