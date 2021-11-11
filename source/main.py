from PyInquirer.utils import print_json
from simplecrypt import encrypt, decrypt, DecryptionException
from userInput import chooseFrom, confirm, getKEY, showActionList, getPassword, askFileLocation
from os import path
import os
from tabulate import tabulate
import pswdManager
import json
import animation
from configuration import getConfig, updateConfig
import shutil

KEY = ""
config = getConfig()
fileLocation = config["fileLocation"]
pswdsBackup = pswdManager.PasswordManager()
pswds = pswdManager.PasswordManager()
animate = animation.Animate()


def encryptPswdData(passwords:dict)->bool:
	# print("\nEncrypting...")
	try:
		passwords_json = json.dumps(passwords)
		animate.startAnimation("Encrypt")
		encryptedPswds = encrypt(KEY, passwords_json)
	except Exception as err:
		print("There was An Exception")
		raise err
	finally:
		animate.stopAnimation()


	try:
		with open(fileLocation, "wb") as f:
			f.write(encryptedPswds)
	except Exception as e:
		print("There was some error while encrypting the data")


def decryptPswdData()->dict:
	# print("\nDecrypting...")
	global fileLocation, pswdsBackup, KEY
	encryptedPswds = ""

	try:
		print(f"this is the file location -> {fileLocation}")
		with open(fileLocation, "rb") as f:
			encryptedPswds = f.readline()
		animate.startAnimation("Decrypt")
		decryptedPswds = decrypt(KEY, encryptedPswds)
		decryptedPswds_str = decryptedPswds.decode("utf-8")
		decryptedPswds_json = json.loads(decryptedPswds_str)
		pswds.passwordsDecrypted = True
		if len(list(decryptedPswds_json.keys())) == 0:
			pswds.setPasswords({})
			pswdsBackup.setPasswords({})
			return {
				"status": "successful",
				"decryptedPswds": {}
			}
		else:
			pswds.setPasswords(decryptedPswds_json)
			pswdsBackup.setPasswords(decryptedPswds_json.copy())
			return {
				"status": "successful",
				"decryptedPswds": decryptedPswds_json
			}

	except FileNotFoundError:
		print("Password file not found... making one")
		encryptPswdData({})
		print("MADE THE PASSWORDS FILE")
		pswds.passwordsDecrypted = True
		return {
			"status": "successful",
			"decryptedPswds": {}
		}
	except DecryptionException as e: 
		errMsg = str(e)
		if errMsg == "Bad password or corrupt / modified data.":
			return {
				"status": "error",
				"msg": errMsg
			}
		elif errMsg == "Passwords File Not found":
			encryptPswdData({})
			print("MADE THE PASSWORD FILE")
			pswds.passwordsDecrypted = True
			return {
				"status": "successful",
				"decryptedPswds": {}
			}
		else:
			print("There was some problem while decrypting the password")
			print("ERROR -> ")
			print(e)
	finally:
		animate.stopAnimation()


def listPswds():
	if pswds.countPassword() == 0:
		print("\nTHERE ARE NO PASSWORDS SAVED")
		return False
	accountNames = [pswd.capitalize() for pswd in list(pswds.getPasswords().keys())]
	accountPasswords = []
	passwords = pswds.getPasswords()
	for accName in accountNames:
		pswd = passwords[accName.lower()]
		accountPasswords.append(pswd)
	print()
	print(
		tabulate(
			{
				"ACCOUNT": accountNames, 
				"PASSWORDS": accountPasswords
			}, 
			headers=["ACCOUNT", "PASSWORDS"]
		)
	)
	print()


def addNewPswd():
	if pswds.passwordsDecrypted == False:
		decryptPswdData()
	accountName = input("ACCOUNT: ").lower().strip()
	if accountExists(accountName):
		if not confirm("The account alredy exists, do you want to overide it"):
			return False
	accountPass = getPassword()
	pswds.addPassword(accountName, accountPass)


def writeChanges():
	passwords = pswds.getPasswords()
	passwordsBackup = pswdsBackup.getPasswords()

	print(passwords)
	print(passwordsBackup)

	if (pswds.countPassword() == 0) or (passwords == passwordsBackup):
		print("\nTHERE ARE NO NEW PASSWORDS TO SAVE")
		return False
	
	encryptPswdData(passwords)
	pswdsBackup.setPasswords(passwords.copy())


def discardChanges():
	if confirm("Do you want to continue \nAll the unsaved changes will be lost"):
		pswds.setPasswords(pswdsBackup.getPasswords().copy())
		print("\nNEW PASSWORDS DISCARDED")


def askUserForKey(msg="Enter KEY:"):
	global KEY
	KEY = getKEY(msg)


def accountExists(account, showInfoMsg=False)->bool:
	if account.lower() in pswds.getPasswords():
		return True
	if showInfoMsg:
		print("\nACCOUNT NOT FOUND")
		print("    1) Check whether account name is spelled correctly")
		print("    2) Check the account exists or not")
	return False


def chooseAccount(msg)->str or bool:
	existingAccounts = list(pswds.getPasswords().keys())
	choosenAccountName = chooseFrom(existingAccounts, msg)
	if choosenAccountName == "EXIT":
		return False
	return choosenAccountName


def deleteAccount():
	account = chooseAccount("Enter the account you want to remove")
	if account:
		ans = confirm(f"Are you sure you want to remove {account}'s password:")
		if ans:
			pswds.delAccount(account)
			print("The account was removed")


def renameAccount():
	oldAccountName = chooseAccount("Enter the account name you want to change")
	if oldAccountName:
		if accountExists(oldAccountName, True):
			newAccountname = input("Enter the new account name: ")
			pswds.renameAccountName(oldAccountName, newAccountname)


def changePassword():
	account = chooseAccount("Enter the account name you want to change")
	if account:
		newPassword = getPassword("Enter new password:")
		pswds.addPassword(account, newPassword)
		print(f"\nPassword for {account} changed successfully!")


def changeKEY():
	global pswdsBackup
	msg = "In order to change the KEY all the changes (if any) will be saved"
	if confirm(msg):
		os.remove(fileLocation)
		askUserForKey("Enter new KEY:")
		passwords = pswds.getPasswords()
		encryptPswdData(passwords)
		pswdsBackup.setPasswords(passwords.copy())
	else:
		return False
		

def moveFile(oldLocation, newLocation):
	shutil.move(oldLocation, newLocation)


def changeFileLocation():
	global fileLocation

	while True:
		newFileLocation = askFileLocation(fileLocation)
		
		if not newFileLocation:
			break

		print(f"This is the new file location \n {newFileLocation}")
		fileExists = path.exists(newFileLocation)
		directoryExists = path.exists(path.dirname(newFileLocation))

		if path.dirname(fileLocation) == newFileLocation:
			print("Enter a different location")
			continue	
		if not directoryExists:
			print(f"Directory {newFileLocation} not found")
			break

		newFileLocation = path.join(newFileLocation, "pswds.bin")
		print("DOES THE FILE EXISTS")
		print(path.isfile(newFileLocation))
		if path.isfile(newFileLocation):
			if fileExists and (not confirm("Do you want to override the existing file")):
				break

		moveFile(fileLocation, newFileLocation)
		updateConfig(newFileLocation)
		fileLocation = newFileLocation
		print("\nLocation changed !")
		break

if __name__ == "__main__":
	if not fileLocation:
		defaultLocation = path.join(path.expanduser("~"), "pswds.bin")
		fileLocation = defaultLocation
		config["fileLocation"] = defaultLocation
		updateConfig(defaultLocation)
	
	while True:
		askUserForKey()
		res = decryptPswdData()
		if res["status"] == "successful":
			break
		else:
			print(res["msg"])
	exit = False

	def endLoop():
		global exit, pswds, pswdsBackup
		if pswds.getPasswords() != pswdsBackup.getPasswords():
			if not confirm("All the unsaved changes will be lost"):
				return False
		exit=True

	actions = {
		"List passwords": listPswds,
		"Add new password": addNewPswd,
		"Write changes": writeChanges,
		"Discard Changes": discardChanges,
		"Delete account": deleteAccount,
		"Rename account": renameAccount,
		"Change file location": changeFileLocation,
		"Change existing password": changePassword,
		"Change KEY": changeKEY,
		"EXIT": endLoop
	}

	while not exit:
		print()
		choice = showActionList()
		actions[choice]()