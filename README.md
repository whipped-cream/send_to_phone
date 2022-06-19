# send_to_phone
A set of Python scripts to upload a file to Transfer.sh and ping a channel on Ntfy with the download link

### Sending files
#### Desktop
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

#### Android
To send files from your phone to your computer a Tasker profile using the Autoshare plugin can probably be set up, but I have not yet purchased it

### Receiving notifications
#### Desktop
Adding this to your Ntfy config file at `/etc/ntfy/client.yml` or `~/.config/ntfy/client.yml` will send a notification via `notify-send` each time a notification is received:
`command: 'notify-send --app-name=Ntfy::"$topic" --icon=terminal "${title:-No title}" "${message:-No message}"'`

#### Android
The Ntfy Android app will allow you to receive Ntfy notifications on your device. Available from the 
[Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy) or [F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy)

[This](taskerprofile://H4sIAAAAAAAAAI1U32+bMBB+Tv4KC6kve8AQIAmRYylq2FRpq6qm3evkgQlWiY1sj6n762cbktD82iSE7+6782ffx4FeiHqjck00AUouPQ8ULVt6oQd0u/QSPzRP7OHxCD1JUbKauqzG2JEHWrr0JhYcobwgmuJwmsTzJJxF8yiaI9gFHVw3WMtf1MSMZSP0WDCdBEGaxgGC9FBQ1mSrsNmjM2yIFThC0Lyts2NFgBME3WoDfEfxoy7fwaPQrGQ50Uxw8ExzylpaIGhxm5e1lGt3iVzwYHgHc0pRUJykqTmltVxso6XLJnLbZ0ceZsKvaP5Ga58bSv9bttmsvmQ/nrP77OF7tkbQVHXlDz2ZKTc9bUltewvPsMkpNqCN9rTnUPwBQtBdzooFe7WsbRV2BdoYyZlc0zAIw0kaDOU6iJNM49Qs82g2FMdokByUsI01bDlVCpwJcOx7IxmeImgX665yp4+7R677zs6GOoRR8E8dXiThqqTSV9UCrMVvXgtSAMIL8Mr/sOaaDi40Qi2R+M4cSEim3xG0rsuFD66JJ1XBDYkm1yX6b/U+sCU9WXABm944yOz6lvMbW6an2L3gBbMKfWWqy2Llvm0/hagDvOJmqDqzCx9KuuE6iuTgEaorhe925ishW/MbsF4PiAbHCIpm70sDVVo3agGhPgoM/U8Iyn0Zgge+y/zhRX7NdH3GHp6yfzaTo4CqiKQFKKXYLcBTJTi9wT/wbcu6cew+cjePdgjxuFu73y0e/wUZvIkyfAUAAA==) Tasker profile will wait for Ntfy notifications from the Ntfy Android app and then automatically download and (sometimes) decompress the files