# send_to_phone
A set of Python scripts to upload a file to Transfer.sh and ping a channel on Ntfy with the download link

### Sending files
#### Linux
Simply run the send_to_phone.py script with the topic on ntfy to publish to and the files to send
```commandline
[michael@HP Send_to_Phone]$ send_to_phone.py --help
usage: send_to_phone.py [-h] [-c] [-ce EMAIL] [-z] [-cl {0,1,2,3,4,5,6,7,8,9}] [--transfersh TRANSFERSH] [--ntfy NTFY] topic files [files ...]

A utility to upload files to Transfer.sh and then ping Ntfy.sh with the download link

positional arguments:
  topic                 Ntfy topic to publish message to
  files                 Files to upload

options:
  -h, --help            show this help message and exit
  -c, --encrypt         Encrypt files before uploading
  -ce EMAIL, --email EMAIL
                        Your email as associated with a key in gpg. Does nothing if --encrypt is not passed
  -z, --compress        Compress files before uploading. Automatically set if more than one filename is passed
  -cl {0,1,2,3,4,5,6,7,8,9}, --compressionlevel {0,1,2,3,4,5,6,7,8,9}
                        Compression level to use. Defaults to 9 if --compress is set, otherwise does nothing
  --transfersh TRANSFERSH
                        Transfer.sh instance to upload file to. Defaults to transfer.sh
  --ntfy NTFY           Ntfy instance to send the message to. Defaults to ntfy.sh
  ```

To install these scripts to your path, create a directory to serve as the install directory and location of the venv,
`/opt/send_to_phone/` for example. Download the scripts to this folder and create a venv, perhaps in `/opt/send_to_phone/venv`. 
Create the environment variable `$SEND_TO_PHONE_INSTALL_DIR` in the usual way to point to this location. 

Then, create the files `transfer`, `ntfy`, and `send_to_phone` somewhere in your `$PATH` with the contents respectively:
```transfer
#!/bin/bash
install_dir=${SEND_TO_PHONE_INSTALL_DIR-/opt/send_to_phone}

$install_dir/venv/bin/python $install_dir/transfer.py "$@"
```

```ntfy
#!/bin/bash
install_dir=${SEND_TO_PHONE_INSTALL_DIR-/opt/send_to_phone}

$install_dir/venv/bin/python $install_dir/ntfy.py "$@"
```

```send_to_phone
#!/bin/bash
install_dir=${SEND_TO_PHONE_INSTALL_DIR-/opt/send_to_phone}

$install_dir/venv/bin/python $install_dir/send_to_phone.py "$@"
```

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

To automatically download and unarchive the files use the following Tasker [project](Send_To_Phone.prj.xml) which will wait for Ntfy notifications from the Ntfy Android app and then automatically download and (sometimes) decompress the files
This project requires Termux, gpg installed via Termux, the Termux:Tasker plugin and requires that you create the file `.termux/tasker/decrypt` in the Termux home directory with the contents:
```shell
gpg -o $2 --decrypt $1
```

Alternatively, simply run [this](setup.sh) following script within Termux to setup everything for you