#2: Python mssql library for running queries
import pyodbc
import pika
import time

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


def db_log(message):
	#Write log to local file
	stamp = time.asctime( time.localtime(time.time()))
	message = stamp + " -> " + message + "\n"
	
	with open('./server_log', 'a') as log_file:
		log_file.write(message)
	
	#Send message to DB for logging
	cred = pika.PlainCredentials('RMQ','RMQ_1234')

	connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
	channel = connection.channel()
	
	channel.exchange_declare(exchange='DB_logs', exchange_type='direct', durable=True)
	channel.basic_publish(exchange='DB_logs', routing_key='', body=message)

	connection.close()

#21-33: Auth function used to see if a user's passwords match up
def auth(uName, pWord):
	query="SELECT password FROM accounts WHERE username='"+uName+"'"
	with cursor.execute(query):
		row=cursor.fetchone()
	try: 
		password=row[0]
		if pWord==password:
			db_log(uName+"logged in")			
			return "true"
		else:
			db_log("User failed to log in")				
			return "false"
	#32-33: If a username doesn't exist in the database, you get a type error if you try to put row[0] in a variable.	
	except TypeError:
		db_log("User failed to log in")			
		return "false"

#36-51: addUser function adds a user's credentials into the database
def addUser(username, password, fName, lName):
	#38-41: Gets a count of the rows and adds one in order to create a primary key for the table
	query1="SELECT COUNT(*) FROM accounts"
	with cursor.execute(query1):
		row=cursor.fetchone()
	count=row[0]+1
	
	#44-51: Inserts the user's row into the database
	query2="INSERT INTO accounts VALUES ("+str(count)+",'"+username+"','"+password+"','"+fName+"','"+lName+"','',0,0,0,0,0,0,0,',,',',,')"
	try:
		cursor.execute(query2)
		connection.commit()
		db_log("User "+username+" was created")			
		return "true"
	#50-51: If a username is already taken, it gives an intergrity error
	except pyodbc.IntegrityError:		
		db_log("Failed to create new user")			
		return "false"

#54-66: addScores adds a user's scores to their account
def addScores(user, timeTrav, songLis, country, edm, hiphop, pop, rock):
	#56-57: Puts the new values into a dictionary to iterate through with the Select statement	
	new=[timeTrav,songLis,country,edm,hiphop,pop,rock]	
	query1="SELECT timeTraveled, songsListenedTo, country, edm, hiphop, pop, rock FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#61-62: Adds the old scores with the new scores to put them back into the table		
		for i in range(len(row)):
			new[i]=new[i]+row[i]
	#64-66: Updates the row with the new scores and commits them
	query2="UPDATE accounts SET timeTraveled="+str(new[0])+", songsListenedTo="+str(new[1])+", country="+str(new[2])+", edm="+str(new[3])+", hiphop="+str(new[4])+", pop="+str(new[5])+", rock="+str(new[6])+" WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("New scores added to "+user)	
	return "true"

#69-81: showScores sends the user's score values to the Front End
def showScores(user):
	resp=''	
	#72-75: Query gets the values from the user's account
	query1="SELECT timeTraveled, songsListenedTo, country, edm, hiphop, pop, rock FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#77-78: Adds the scores into a string seperated by commas	
		for i in row:
			resp=resp+","+str(i)
	#79-81:Adds the username to the string and returns the whole string	
	resp=user+resp
	db_log("User "+user+" checked their scores")		
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
			db_log("User "+user+" failed to add friend")	
			return "false"
	#101-110: First checks if the friends are already added. Then adds the userID to each person's friends list
	if useID2 in currFriends1:	
		db_log("User "+user+" failed to add friend")			
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
	db_log("User "+user+" added new friend "+friend)	
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
	try:	
		for i in range(len(friendList)):
			query="SELECT username FROM accounts WHERE userID='"+friendList[i]+"'"
			with cursor.execute(query):
				row=cursor.fetchone()
				friendList[i]=str(row[0])
	except TypeError:
		db_log("User "+user+" checked his friends list")		
		return 'No friends'
	#135-141: Iterates though the list again to put the values into a string to send to the front end
	friendsShow=''	
	for i in range(len(friendList)):
		if friendsShow=='':
			friendsShow=friendList[i]
		else:
			friendsShow=friendsShow+","+friendList[i]
	db_log("User "+user+" checked his friends list")
	return friendsShow

#144-160: saveRoute takes the time of a user's favorite route and replaces the old one he first put in with the new one
def saveRoute(user, route):
   	#146-154: Fetches the current faveRoute list and adds the new route to it and takes out the oldest		
	query1="SELECT faveRoute FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currRoutes=row[0]
	currRoutes=currRoutes.split(',')
	
	currRoutes[0]=currRoutes[1]
	currRoutes[1]=currRoutes[2]
	currRoutes[2]=route
	#156-160: Puts the newRoute list into the accounts table
	newRoute=currRoutes[0]+","+currRoutes[1]+","+currRoutes[2]
	query2="UPDATE accounts SET faveRoute='"+newRoute+"' WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("User "+user+" saved a new route")	
	return "true"

#163-170: selectRoute returns a specific route based on which route the user wants
def selectRoute(user, route):
	#165-170: Gets the faveRoute list and selects which one based on the parameter route
	query1="SELECT faveRoute FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currRoutes=str(row[0])
	currRoutes=currRoutes.split(',')
	db_log("User "+user+" checked his routes")	
	return currRoutes[route]

#173-189: savePlaylist takes the ID of a user's favorite playlist and replaces the old one he first put in with the new one
def savePlaylist(user, playlist):
	#175-183: Fetches the current favePlaylist list and adds the new playlist to it and takes out the oldest		
	query1="SELECT favePlaylist FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currPlaylists=row[0]
	currPlaylists=currPlaylists.split(',')
	
	currPlaylists[0]=currPlaylists[1]
	currPlaylists[1]=currPlaylists[2]
	currPlaylists[2]=playlist
	#185-189: Puts the newPlaylists list into the accounts table
	newPlaylists=currPlaylists[0]+","+currPlaylists[1]+","+currPlaylists[2]
	query2="UPDATE accounts SET favePlaylist='"+newPlaylists+"' WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("User "+user+" saved a new playlist")	
	return "true"

#192-199: selectPlaylist returns a specific playlist based on which playlist the user wants
def selectPlaylist(user, playlist):
	#165-170: Gets the favePlaylist list and selects which one based on the parameter playlist
	query1="SELECT favePlaylist FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currPlaylists=str(row[0])
	currPlaylists=currPlaylists.split(',')
	db_log("User "+user+" checked his playlists")	
	return currPlaylists[playlist]
