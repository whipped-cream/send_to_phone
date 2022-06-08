import requests
import os
import argparse
import tarfile
import gzip

def transfer(filename: str, instance: str) -> str:
    basename = os.path.basename(filename)
    filepath = os.path.abspath(filename)
    file = open(filepath, 'rb')

    upload_url = 'https://' + instance + '/' + basename
    try:
        response = requests.put(upload_url, file)
    except:
        print('Error: unable to transfer file')
        exit(1)

    return response.text


def archive(files: list) -> str:
    tarname = 'temp' + str(os.getpid()) + '.tar'
    cache_dir = os.environ.get('XDG_CACHE_HOME')
    if cache_dir is None:
        cache_dir = '.cache'
        os.mkdir(cache_dir)
    else:
        cache_dir += '/send_to_phone'
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    tarpath = cache_dir + '/' + tarname
    tar = tarfile.open(tarpath, "w:gz")

    for file in files:
        filepath = os.path.abspath(file)
        basename = os.path.basename(file)
        tar.add(filepath, basename)

    tar.close()

    return tarpath


def encrypt(file: str, key_path: str, ) -> str:
    print('TODO')
    return file
    # do something


def encrypt(file: str, password: str) -> str:
    print('TODO')
    return file
    # do something


def process_and_upload(files: list, args):
    print('TODO')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Utility to upload files to transfer.sh')
    parser.add_argument('files', nargs='+', help='Files to upload')
    parser.add_argument('-c', '--encrypt', action='store_true', help='Encrypt files before uploading')
    parser.add_argument('-z', '--compress', action='store_true',
                        help='Compress files before uploading. Automatically set if more than one filenames is passed')
    parser.add_argument('--instance', help='Instance to upload file to. Defaults to transfer.sh', default='transfer.sh')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if len(args.files) > 1 or args.compress:
        file = archive(args.files)
    else:
        file = args.files[0]

    if args.encrypt:
        file = encrypt(file, 'password')

    download_url = transfer(file, args.instance)

    print(download_url)

