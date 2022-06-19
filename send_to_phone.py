#!/usr/bin/env python
from ntfy import publish
from transfer import process_and_upload
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='A utility to upload files to Transfer.sh and then ping Ntfy.sh with the download link')
    parser.add_argument('topic', help='Ntfy topic to publish message to')
    parser.add_argument('files', nargs='+', help='Files to upload')
    parser.add_argument('-c', '--encrypt', action='store_true', help='Encrypt files before uploading', default=False)
    parser.add_argument('-z', '--compress', action='store_true',
                        help='Compress files before uploading. Automatically set if more than one filename is passed',
                        default=False)
    parser.add_argument('--transfersh', help='Transfer.sh instance to upload file to. Defaults to transfer.sh',
                        default='transfer.sh')
    parser.add_argument('--ntfy', help='Ntfy instance to send the message to. Defaults to ntfy.sh', default='ntfy.sh')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    download_url = process_and_upload(args.files, args.encrypt, args.compress, args.transfersh)
    print(download_url)

    publish(args.topic, download_url, title='Files shared from: {0}'.format(os.uname().nodename), instance=args.ntfy)
