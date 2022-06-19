#!/usr/bin/env python
import os
import desktop_notifier
import asyncio
import requests
import argparse
import webbrowser


def download_from_transfersh(message: str) -> None:
    file_request = requests.get(message)
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads\\"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads/"
    open(DOWNLOAD_FOLDER + message[message.rfind('/') + 1:], 'wb').write(file_request.content)
    # Thanks to Kieran Wood on https://stackoverflow.com/a/69052674


def open_in_browser(url: str) -> None:
    webbrowser.open(url)


async def send_notification(title: str, message: str, app_name: str) -> None:
    notifier = desktop_notifier.DesktopNotifier(
        app_name=app_name
    )

    buttons: [desktop_notifier.Button] = []
    if message.startswith('https://transfer.sh/'):
        buttons.append(
            desktop_notifier.Button(
                title='Download file',
                on_pressed=lambda: download_from_transfersh(message))),
    elif message.startswith('https://'):
        buttons.append(
            desktop_notifier.Button(
                title='Open in browser',
                on_pressed=lambda: open_in_browser(message))),

    await notifier.send(
        title=title,
        message=message,
        buttons=buttons
    )


def parse_args():
    parser = argparse.ArgumentParser(description='A utility to handle notifications send from the send_to_phone '
                                                 'Python script')
    parser.add_argument('message', help='Body of the notification')
    parser.add_argument('-t', '--title', help='Title of the notification', default='No title')
    parser.add_argument('--app-name', help='App name of the notification', default='Python app')
    return parser.parse_args()


async def wait(seconds: int):
    await asyncio.sleep(seconds)


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.create_task(send_notification(args.title, args.message, args.app_name))
    loop.run_until_complete(wait(10))
    # todo: figure out how to make a daemon that can respond to the notifications and not close after a while
