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

#21-33: Auth function used to see if a user's passwords match up
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
#35-52: addUser function adds a user's credentials into the database
def addUser(username, password, fName, lName):
	#37-40: Gets a count of the rows and adds one in order to create a primary key for the table
	query1="SELECT COUNT(*) FROM accounts"
	with cursor.execute(query1):
		row=cursor.fetchone()
	count=row[0]+1
	
	#43-52: Inserts the user's row into the database
	query2="INSERT INTO accounts VALUES ("+str(count)+",'"+username+"','"+password+"','"+fName+"','"+lName+"','',0,0,0,0,0,0,0,'',0)"
	try:
		cursor.execute(query2)
		connection.commit()
		print "Account created!"
		return "Account created!"
	#50-52: If a username is already taken, it gives an intergrity error
	except pyodbc.IntegrityError:
		print "Username is already in use"		
		return "Username is already in use"
