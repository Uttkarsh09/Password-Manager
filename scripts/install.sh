#!/bin/sh
echo "-----RUNNING pipenv install"
sleep 1s
pipenv install
echo "-----RUNNING pip uninstall pycrypto"
sleep 1s
echo -ne '\n' | pip uninstall pycrypto
sleep 1s
echo "-----RUNNING pipenv install pycryptodome==3.11.0"
pip install -U pycryptodome
