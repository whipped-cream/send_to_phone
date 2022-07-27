#!/data/data/com.termux/files/usr/bin/bash
termux-setup-storage

mkdir -p .termux/tasker
pkg update && pkg install gnupg
echo 'gpg -o $2 --decrypt $1' > .termux/tasker/decrypt
chmod +x .termux/tasker/decrypt
