from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt, print_json, style_from_dict, Separator
from examples import custom_style_1, custom_style_2
import os

def getKEY()->str:
    questions = [
        {
            "type": "password",
            "message": "Enter KEY:",
            "name": "KEY"
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    KEY = answers["KEY"]
    return KEY


def getPassword()->str:
    questions = [
        {
            "type": "password",
            "message": "Enter password:",
            "name": "password"
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    password = answers["password"]
    return password


def confirm(message)->bool:
    questions = [
            {
                    "type": "confirm",
                    "message": message,
                    "name": "continue",
                    "default": True,
            }
    ]
    answers = prompt(questions, style=custom_style_1)
    return answers["continue"]


def chooseFrom(choices:list, message:str)->str:
    choices.append("EXIT")
    options = [
        {
            "type": "list",
            "name": "account",
            "message": message,
            "choices": choices,
        }
    ]
    choice = prompt(options, style=custom_style_2)
    choice = choice["account"]
    return choice


def askFileLocation(currFileLocation:str):
    print(f"Current file location: {currFileLocation}")
    options = ["Enter new password file location", "Use Default", "EXIT"]
    choice = [
        {
            "type": "list",
            "name": "fileLocationChoice",
            "message": "Change file location",
            "choices": options
        }
    ]
    choice = prompt(choice, style=custom_style_2)
    choice = choice["fileLocationChoice"]
    
    if choice == options[2]:
        return False

    if choice == options[1]:
        return os.path.expanduser("~")

    if choice == options[0]:
        questions = [
            {
                "type": "input",
                # This looks ugly as s**t.....i know
                "message": """Enter new file location 
    Example:- 
        /new/file/location/
:""",
                "name": "fileLocation"
            }
        ]
        answer = prompt(questions, style=custom_style_2)
        newFileLocation = answer["fileLocation"]
        return newFileLocation


def showActionList():
    questions = [
        {
            "type": "list",
            "name": "choice",
            "message": "Action to perform",
            "choices": [
                "List passwords",
                "Add new password",
                "Change existing password",
                "Delete account",
                "Rename account",
                "Change file location",
                "Write changes",
                "Discard Changes",
                "Change KEY",
                "EXIT",
            ]
        }
    ]
    choice = prompt(questions, style=custom_style_2)
    choice = choice["choice"]
    return choice