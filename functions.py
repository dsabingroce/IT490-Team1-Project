import sys
import os
import subprocess

def auth(username, password):
	log="sqlcmd -S localhost -U SA -P 'D3rz3tAbe!in' -Q 'SELECT password FROM accounts WHERE username=\""+username+"\"'"
	result = subprocess.check_output(log, shell=True)
	result=result.split('-')
	result=result[255].split(' ')
	result=result[0].split('\n')
	if password==result[1]:	
		return 1
	else:	
		return 0

def addUser(username, password, fName, lName):
	log="sqlcmd -S localhost -U SA -P 'D3rz3tAbe!in' -Q 'SELECT COUNT(*) FROM accounts'"
	result = subprocess.check_output(log, shell=True)
	result=result.split('-')
	result=result[11].split(' ')
	result=result[10].split('\n')
	numrows=int(result[0])+1
	query="sqlcmd -S localhost -U SA -P \'D3rz3tAbe!in\' -Q \"INSERT INTO accounts(userID, username, password, fName, lName) VALUES ("+str(numrows)+",\'"+username+"\',\'"+password+"\',\'"+fName+"\',\'"+lName+"\')\""
	resp=subprocess.check_output(query, shell=True)	
	if "Msg 2627" in resp:
		print "Username already exists"
	else:
		print resp

def addFriend(username, fUsername):
	query="sqlcmd -S localhost -U SA -P \'D3rz3tAbe!in\' -Q \""
