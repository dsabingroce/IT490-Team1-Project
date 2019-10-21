#2: Python mssql library for running queries
import pyodbc

#5-15: Connecting to Database
details = {
 'server' : 'localhost',
 'database' : 'projectDB',
 'username' : 'SA',
 'password' : 'D3rz3tAbe!in',
 'connection' : 'no'
 }

connect_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};PORT=1443; DATABASE={database};UID={username};PWD={password};Trusted_connection={connection};)'.format(**details)

connection = pyodbc.connect(connect_string)

#18: Cursor runs queries and fetches rows
cursor = connection.cursor()

#21-32: Auth function used to see if a user's passwords match up
def auth(uName, pWord):
	query="SELECT password FROM accounts WHERE username='"+uName+"'"
	with cursor.execute(query):
		row=cursor.fetchone()
	try: 
		password=row[0]
		if pWord==password:
			return "Passwords match!"
		else:
			return "Passwords do not match!"
	#32-33: If a username doesn't exist in the database, you get a type error if you try to put row[0] in a variable.	
	except TypeError:
		return "Username does not exist!"

def addUser(uName, pWord, first, last):
	query1="SELECT COUNT(*) FROM accounts"
	with cursor.execute(query1):
		row=cursor.fetchone()
	count=row[0]+1
	
	#Current problem: Query 2 isn't a query?
	query2="INSERT INTO accounts (userID,username,password,fName,lName) VALUES ("+str(count)+",\'"+uName+"\',\'"+pWord+"\',\'"+first+"\',\'"+last+"\');"
	print query2
	with cursor.execute(query2):
		row2=cursor.fetchone()
	print row2[0]

addUser("test4", "efgh", "Tim", "Scott")
