#! /bin/bash

saffron stop
rm -rf ~/.lamden/*
unset LAMDEN_HOME
unset LAMDEN_FOLDER_PATH
unset LAMDEN_DB_FILE
saffron init newCoin
source ~/.lamden/newCoin/newCoin.source
saffron start newCoin
cp -R ./saffron/contracts ~/.lamden/newCoin
saffron deploy