#!/data/data/com.termux/files/usr/bin/bash
termux-setup-storage

pkg update && pkg install gnupg

mkdir -p .termux/tasker
echo 'gpg -o $2 --decrypt $1' > .termux/tasker/decrypt
chmod +x .termux/tasker/decrypt
