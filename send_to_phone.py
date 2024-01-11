#!/usr/bin/env python
from ntfy import publish
from transfer import process_and_upload
import argparse
import os
import platform

def parse_args():
    parser = argparse.ArgumentParser(
        description='A utility to upload files to Transfer.sh and then ping Ntfy.sh with the download link')
    parser.add_argument('topic', help='Ntfy topic to publish message to')
    parser.add_argument('files', nargs='+', help='Files to upload')
    parser.add_argument('-c', '--encrypt', action='store_true', help='Encrypt files before uploading', default=False)
    parser.add_argument('-ce', '--email', help='Your email as associated with a key in gpg. Does nothing if --encrypt '
                                               'is not passed')
    parser.add_argument('-z', '--compress', action='store_true',
                        help='Compress files before uploading. Automatically set if more than one filename is passed',
                        default=False)
    parser.add_argument('-cl', '--compressionlevel', help='Compression level to use. Defaults to 9 if --compress is '
                                                          'set, otherwise does nothing', default=9, choices={0, 1, 2,
                                                                                                             3, 4, 5,
                                                                                                             6, 7, 8,
                                                                                                             9})
    parser.add_argument('--transfersh', help='Transfer.sh instance to upload file to. Defaults to transfer.whalebone.io',
                        default='transfer.whalebone.io')
    parser.add_argument('--ntfy', help='Ntfy instance to send the message to. Defaults to ntfy.sh', default='ntfy.sh')
    args = parser.parse_args()
    if args.encrypt and args.email is None:
        parser.error('Encrypt requires an email address')
    return args


if __name__ == "__main__":
    args = parse_args()

    download_url = process_and_upload(files=args.files, encrypt_flag=args.encrypt, encryption_email=args.email, compress_flag=args.compress, instance=args.transfersh)
    print(download_url)

    publish(topic=args.topic, message=download_url, title='Files shared from: {0}'.format(platform.node()), instance=args.ntfy)
