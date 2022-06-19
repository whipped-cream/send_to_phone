# send_to_phone
A set of Python scripts to upload a file to Transfer.sh and ping a channel on Ntfy with the download link

### Sending files
#### Linux
Simply run the send_to_phone.py script with the topic on ntfy to publish to and the files to send
```
[michael@HP ~]$ send_to_phone.py --help
usage: send_to_phone.py [-h] [-c] [-z] [--transfersh TRANSFERSH] [--ntfy NTFY] topic files [files ...]

A utility to upload files to Transfer.sh and then ping Ntfy.sh with the download link

positional arguments:
  topic                 Ntfy topic to publish message to
  files                 Files to upload

options:
  -h, --help            show this help message and exit
  -c, --encrypt         Encrypt files before uploading
  -z, --compress        Compress files before uploading. Automatically set if more than one filename is passed
  --transfersh TRANSFERSH
                        Transfer.sh instance to upload file to. Defaults to transfer.sh
  --ntfy NTFY           Ntfy instance to send the message to. Defaults to ntfy.sh
  ```

It may be worth editing the first line of the files to run in a venv. For example, for a venv in `/opt/send_to_phone/venv/` replace the first line of each of the python files with:

`#!/opt/send_to_phone/venv/bin/python`. 

Alternatively a simple shell wrapper can be created that runs the scripts and does not require updating the scripts each time the scripts get updated.

Placing the scripts anywhere in your $PATH will allow them to be run from anywhere, preferably `/usr/local/bin/`

##### KDE
If you use KDE you can add a ServiceMenu so that the action will appear in some context menus.

Create the file `$HOME/.local/share/kservices5/ServiceMenus/share_to_phone.desktop` with the contents:

```send_to_phone.desktop
[Desktop Entry]
Type=Service
Icon=stock_shared-by-me
X-KDE-ServiceTypes=KonqPopupMenu/Plugin
MimeType=all/allfiles;
Actions=send_to_phone;
Encoding=UTF-8

[Desktop Action send_to_phone]
Name=Send files to Phone
Icon=stock_shared-by-me
Exec=dbusRef=`kdialog --progressbar "Uploading files"` && send_to_phone.py $NTFY_CHANNEL %F && qdbus $dbusRef close
```
Replacing `$NTFY_CHANNEL` with your chosen Ntfy channel

#### Windows
Create a batch script in the location of your venv with the contents:

```send_to_phone.bat
pushd C:\path\to\install\folder
.\venv\Scripts\python.exe .\send_to_phone.py $NTFY_CHANNEL %*
```

and then create a shortcut to this file at `%AppData%\Microsoft\Windows\SendTo\Phone`

#### Android
To send files from your phone to your computer a Tasker profile using the Autoshare plugin can probably be set up, but I have not yet purchased it

### Receiving notifications
#### Desktop
Adding this to your Ntfy config file at `/etc/ntfy/client.yml` or `~/.config/ntfy/client.yml` will send a notification via `notify-send` each time a notification is received:
`command: 'notify-send --app-name=Ntfy::"$topic" --icon=terminal "${title:-No title}" "${message:-No message}"'`

#### Android
The Ntfy Android app will allow you to receive Ntfy notifications on your device. Available from the 
[Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy) or [F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy)

To automatically download and unarchive the files use the following Tasker [profile](Ntfy_Notification_Received.prf.xml) and associated [tasks](Transfer.sh__Download_and_Unzip.tsk.xml) which will wait for Ntfy notifications from the Ntfy Android app and then automatically download and (sometimes) decompress the files