#!/bin/bash
export TELEGRAM_ENCRYPT_FILE=".keys/telegram_token.bin"
export WEATHERSTACK_ENCRYPT_FILE=".keys/weatherstack_token.bin"

# This script need a master key, you have to pass one o more arrguments.
if [ "$#" -eq 0 ]; then
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    echo "+ You need a master password, run: \$ openssl rand -base64 32 > key.bin+"
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return
fi

if [ ! -d .keys ]; then
  mkdir -p .keys;
fi
# If no exist a encripted token for Telgram or Weatherstack
if [ "$#" -eq 3 ] || [ ! -f $TELEGRAM_ENCRYPT_FILE ] || [ ! -f $TELEGRAM_ENCRYPT_FILE ]; then
  tmpfile=$(mktemp)
  echo $2 > $tmpfile
  openssl enc -aes-256-cbc -salt -in $tmpfile -out $TELEGRAM_ENCRYPT_FILE -pass file:$1
  echo $3 > $tmpfile
  openssl enc -aes-256-cbc -salt -in $tmpfile -out $WEATHERSTACK_ENCRYPT_FILE -pass file:$1
  rm "$tmpfile"
elif [ "$#" -ne 1 ]; then
  echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  echo "+ The number of arguments is incorrect.                                  +"
  echo "+ You need a crete encrypted tokenes, please see the documentation       +"
  echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  return
fi

# It create a enviroment variables for the tokens.
file="$1"
line=$(head -n 1 $file)
export MASTER_PASSWORD=$(echo $line)

tmpfile=$(mktemp)
openssl enc -d -aes-256-cbc -salt -in $TELEGRAM_ENCRYPT_FILE -out $tmpfile -pass file:$1
export TELEGRAM_TOKEN="$(cat $tmpfile)"
openssl enc -d -aes-256-cbc -salt -in $WEATHERSTACK_ENCRYPT_FILE -out $tmpfile -pass file:$1
export WEATHERSTACK_TOKEN="$(cat $tmpfile)"
rm "$tmpfile"
