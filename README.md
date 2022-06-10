# send_to_phone
A set of Python scripts to upload a file to Transfer.sh and ping a channel on Ntfy with the download link

### Receiving notifications
#### Android
[This](taskerprofile://H4sIAAAAAAAAAI2U3Y6bMBCFr5OnsJD2phcYQyCwciytNqiK1K6qzba3lQUmsZbYyLaotk9f25D/Jq0Uwdhnhpmcz4DfqH5nakkNBVotggDUPV8EKACmXwRpiOxvFpDpBH9TsuEt81mdjZMA9GwRxE6c4KqmhhGUpbM8RfMkT5Icw2HTyewoZwileYRmGLKD3LR0o4mtGAK3xWuSYGivbrHjdURSDP3dbYgdIy+m+QAv0vCGV9RwKcArqxjvWY2h011e2TNh/MiVFNHpxHZkWTOSFoWd00V+b22Uz6ZqM2YnAeEy3LLqnbWhsC3Dr+V6/fS5/PlaPperH+USQ1s1lK/GZrbcOtjT1jkJr7T4Ujtpm+zbXkuzMwlD/+ccGjiycbHj6QuMDdIrOBmKEIqL6CacKI/jrDiFYxmkBxLOWNutYlqDKwBH358qD8QPXpnRyvmp8SiJ/mn8m6JCN0yFevsIlvKXaCWtARU1+C5+8+6W8X5rgnuqyEOnuFTcfGDolj4XrrxrF1XRHSbxbSb/jeusWzo2i/6iZXcGmd9+ZH7nkcWl9ixFzR2hL1wPWbzZ23bQhtfmSMPLE9xuNXnYWf50wzB0q1GQHbEvtb2Oa2WlrTGdfoTQHEnC8BOGal) 
Tasker profile will wait for Ntfy notifications from the [Ntfy Android app](https://play.google.com/store/apps/details?id=io.heckel.ntfy) and then automatically download and (sometimes) decompress the files

#### Desktop
Adding this to your Ntfy config file at `/etc/ntfy/client.yml` or `~/.config/ntfy/client.yml` will send a notification via `notify-send` each time a notification is received:
`command: 'notify-send --app-name=Ntfy::"$topic" --icon=terminal "${title:-No title}" "${message:-No message}"'`

