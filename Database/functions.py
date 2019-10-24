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
			return "true"
		else:
			return "false"
	#32-33: If a username doesn't exist in the database, you get a type error if you try to put row[0] in a variable.	
	except TypeError:
		return "false"

#36-51: addUser function adds a user's credentials into the database
def addUser(username, password, fName, lName):
	#38-41: Gets a count of the rows and adds one in order to create a primary key for the table
	query1="SELECT COUNT(*) FROM accounts"
	with cursor.execute(query1):
		row=cursor.fetchone()
	count=row[0]+1
	
	#44-51: Inserts the user's row into the database
	query2="INSERT INTO accounts VALUES ("+str(count)+",'"+username+"','"+password+"','"+fName+"','"+lName+"','',0,0,0,0,0,0,0,'',0)"
	try:
		cursor.execute(query2)
		connection.commit()
		return "true"
	#50-51: If a username is already taken, it gives an intergrity error
	except pyodbc.IntegrityError:		
		return "false"

#54-66: addScores adds a user's scores to their account
def addScores(user, timeTrav, songLis, pop, rock, country, hiphop, edm):
	#56-57: Puts the new values into a dictionary to iterate through with the Select statement	
	new=[timeTrav,songLis,pop,rock,country,hiphop,edm]	
	query1="SELECT timeTraveled, songsListenedTo, pop, rock, country, hiphop, edm FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#61-62: Adds the old scores with the new scores to put them back into the table		
		for i in range(len(row)):
			new[i]=new[i]+row[i]
	#64-66: Updates the row with the new scores and commits them
	query2="UPDATE accounts SET timeTraveled="+str(new[0])+", songsListenedTo="+str(new[1])+", pop="+str(new[2])+", rock="+str(new[3])+", country="+str(new[4])+", hiphop="+str(new[5])+", edm="+str(new[6])+" WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	return "true"

#69-81: showScores sends the user's score values to the Front End
def showScores(user):
	resp=''	
	#72-75: Query gets the values from the user's account
	query1="SELECT timeTraveled, songsListenedTo, pop, rock, country, hiphop, edm FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#77-78: Adds the scores into a string seperated by commas	
		for i in row:
			resp=resp+","+str(i)
	#79-81:Adds the username to the string and returns the whole string	
	resp=user+resp	
	return resp

#84-118: addFriend takes two usernames and updates the database to add each of those users in their friends column
def addFriend(user, friend):
	#86-99: Fetches the current friends list and userID of both the user and the friend they want to add.	
	query1="SELECT friends, userID FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currFriends1=str(row[0])	
		useID1=str(row[1])
	query2="SELECT friends, userID FROM accounts WHERE username='"+friend+"'"
	with cursor.execute(query2):
		row=cursor.fetchone()
		#95-99: If the username put in does not exist, we get a TypeError		
		try:		
			currFriends2=str(row[0])	
			useID2=str(row[1])
		except TypeError:
			return "false"
	#101-110: First checks if the friends are already added. Then adds the userID to each person's friends list
	if useID2 in currFriends1:	
		return "false"
	if currFriends1=='':
		newFriends1=useID2
	else:
		newFriends1=currFriends1+","+useID2
	if currFriends2=='':
		newFriends2=useID1
	else:
		newFriends2=currFriends2+","+useID1	
	#112-118: Updates the accounts with the new friends list
	query3="UPDATE accounts SET friends='"+newFriends1+"' WHERE username='"+user+"'"
	cursor.execute(query3)
	connection.commit()
	query4="UPDATE accounts SET friends='"+newFriends2+"' WHERE username='"+friend+"'"
	cursor.execute(query4)
	connection.commit()
	return "true"

#121-141: showFriends gives the usernames of a person's friends
def showFriends(user):
	#123-127: Gets the friends string from the account and convert it into a list
	query1="SELECT friends FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		friends=str(row[0])
	friendList=friends.split(',')
	#129-133: Iterates through the list to get the usernames and put them into the old list
	for i in range(len(friendList)):
		query="SELECT username FROM accounts WHERE userID='"+friendList[i]+"'"
		with cursor.execute(query):
			row=cursor.fetchone()
			friendList[i]=str(row[0])	
	#135-141: Iterates though the list again to put the values into a string to send to the front end
	friendsShow=''	
	for i in range(len(friendList)):
		if friendsShow=='':
			friendsShow=friendList[i]
		else:
			friendsShow=friendsShow+","+friendList[i]
	return friendsShow
