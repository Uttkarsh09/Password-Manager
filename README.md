
# Password Manager 🔐

A simple password manager to save all your passwords.


So this is a project I started a long long time ago ⌛, for time pass, and left it in between.....😅.

Fast forward to November 2021, I finally completed it with dropping a few of the functionalities (just a few minor ones I promise🤫).

## Details ℹ️

All the passwords are saved in a form of cyphertext, secured by a master password, so don't worry even if someone steals your passwods file.

I have used python's [simple-crypt](https://pypi.org/project/simple-crypt/) module for all the encryptions.

## Setup ℹ️
1. Before beginning you should have [pipenv](https://pypi.org/project/pipenv/) installed.
2. Make sure that ```./scripts/install.sh``` has execution permission.
3. Open the terminal/console, move to the project directory and execute ```pipenv shell```.
4. You should now be in the virtual environment of this project, run ```pipenv run config``` to install the required modules and configure them.
5. Once all this is done run ```pipenv run start```.

## Possible Problems 🚩
1. If you are in the virtual environment and using a text editor like VSCode and you get warning like module not found (from the text editor), change the python interpreter with the location of the virtual environment.
2. Not tested in Windows OS 😥.
