import json
from userInput import confirm, getKEY, showActionList, getPassword
from simplecrypt import encrypt, decrypt, DecryptionException

class PasswordManager:
	def __init__(self) -> None:
		self.passwords:dict = {}
		self.passwordsDecrypted:bool = False
		
	def countPassword(self)->int:
		return len(list(self.passwords.keys()))


	def getPasswords(self)->dict:
		return self.passwords
	

	def setPasswords(self, newPasswords:dict)->bool:
		self.passwords = newPasswords
		return True


	def delAccount(self, accountName:str)->bool:
		del self.passwords[accountName]
		return True


	def renameAccountName(self, oldAccountName:str, newAccountName:str)->bool:
		oldAccountName = oldAccountName.lower()
		newAccountName = newAccountName.lower()
		password = self.passwords[oldAccountName]
		del self.passwords[oldAccountName]
		self.passwords[newAccountName] = password

	# This method is used for both adding passwords and changing it
	# As the logic is the same
	def addPassword(self, account:str, password:str):
		self.passwords[account] = password