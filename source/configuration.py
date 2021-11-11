import json
import shutil

def getConfig():
    try:
        with open("./source/settings.json", "r") as f:
            config = f.read()
            config = json.loads(config)
            return config
    except Exception as e:
        print(e)


def updateConfig(newFileLocation:str):
    try:
        config = getConfig()
        with open("./source/settings.json", "w") as f:
            config["fileLocation"] = newFileLocation
            f.write(json.dumps(config, indent=4))
        return True
    except Exception as e:
        print(e)
        return False