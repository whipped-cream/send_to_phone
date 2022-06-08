import requests
import os
import argparse
import tarfile
import gzip

def transfer(filename: str, instance: str) -> str:
    basename = os.path.basename(filename)
    filepath = os.path.abspath(filename)
    file = open(filepath, 'rb')

    upload_url = instance + filename
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
        file = os.path.abspath(file)
        tar.add(file)

    tar.close()

    return tarpath


def encrypt(files: list, key_path: str, ) -> object:
    print('TODO')
    # do something


def encrypt(files: list, password: str) -> object:
    print('TODO')
    # do something


if __name__ == "__main__":
    tarpath = archive({'file1', 'file2', 'file3'})
    url = transfer(tarpath, 'https://transfer.sh/')
    print(url)
    os.remove(tarpath)

    # parser = argparse.ArgumentParser(
    #     description='Utility to upload files to transfer.sh')
    # parser.add_argument('files', nargs='+', help='Files to upload')
    # parser.add_argument('-c', '--encrypt', action='store_true', help='Encrypt files before uploading')
    # parser.add_argument('-z', '--compress', help='Compress files before uploading. Automatically set if more than one filenames is passed')
    # args = parser.parse_args()
