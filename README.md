# send_to_phone
A set of Python scripts to upload a file to Transfer.sh and ping a channel on Ntfy with the download link

### Receiving notifications
Adding this to your Ntfy config file at `/etc/ntfy/client.yml` or `~/.config/ntfy/client.yml` will send a notification via `notify-send` each time a notification is received:
`command: 'notify-send --app-name=Ntfy::"$topic" --icon=terminal "${title:-No title}" "${message:-No message}"'`