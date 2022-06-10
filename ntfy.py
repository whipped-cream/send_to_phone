#!/usr/bin/env python
import argparse
import requests


def publish(topic: str, message: str, title: str = 'No title', priority: str = '3', tags=None,
            instance: str = 'ntfy.sh'):
    if tags is None:
        tags = {}
    url = 'https://{0}/{1}'.format(instance, topic)

    requests.post(url,
                  data=message,
                  headers={
                      "Title": title,
                      "Priority": str(priority),
                      "Tags": ','.join('{}'.format(tag) for tag in tags)
                  })


def parse_args():
    parser = argparse.ArgumentParser(description='Utility to publish notifications to Ntfy.sh')
    parser.add_argument('topic', help='Ntfy topic to publish message to')
    parser.add_argument('message', help='Message body')
    parser.add_argument('-t', '--title', help='Title of the message', default='No title')
    parser.add_argument('--priority', help='Priority of the message', default=3, choices=['1', '2', '3', '4', '5'])
    parser.add_argument('--tags', nargs='*', help='Tags of the message', default=None)
    parser.add_argument('--instance', help='Instance to send the message to. Defaults to ntfy.sh', default='ntfy.sh')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    publish(args.topic, args.message, args.title, args.priority, args.tags, args.instance)
