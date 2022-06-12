#!/usr/bin/env python
import os
import desktop_notifier
import asyncio
import requests

def download_from_transfersh(message: str) -> None:
    file_request = requests.get(message)
    if os.name == "nt":
        DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads\\"
    else:  # PORT: For *Nix systems
        DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads/"
    open(DOWNLOAD_FOLDER + message[message.rfind('/')+1:], 'wb').write(file_request.content)


def open_in_browser(url: str) -> None:
    os.system('xdg-open ' + url)


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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_notification('Title', 'https://transfer.sh/PDQQwl/Send%20to%20phone.md', 'Test App'))
    loop.run_forever()



