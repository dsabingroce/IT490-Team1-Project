#2: Python mssql library for running queries
import pyodbc
import pika
import time

#7-17: Connecting to Database
details = {
 'server' : 'localhost',
 'database' : 'projectDB',
 'username' : 'SA',
 'password' : 'D3rz3tAbe!in',
 'connection' : 'no'
 }

connect_string = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};PORT=1443; DATABASE={database};UID={username};PWD={password};Trusted_connection={connection};)'.format(**details)

connection = pyodbc.connect(connect_string)

#20: Cursor runs queries and fetches rows
cursor = connection.cursor()

#23-40: db_log writes a log to a local file both on the system and in a master file 
def db_log(message):
	#25-29: Writes log to local file
	stamp = time.asctime( time.localtime(time.time()))
	message = stamp + " -> " + message
	
	with open('./server_log', 'a') as log_file:
		log_file.write(message+"\n")
		
	#32-40: Sends message to DB for logging
	cred = pika.PlainCredentials('RMQ','RMQ_1234')

	connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
	channel = connection.channel()
	
	channel.exchange_declare(exchange='DB_logs', exchange_type='direct', durable=True)
	channel.basic_publish(exchange='DB_logs', routing_key='', body=message)

	connection.close()
	print message

#44-59: Auth function used to see if a user's passwords match up
def auth(uName, pWord):
	query="SELECT password FROM accounts WHERE username='"+uName+"'"
	with cursor.execute(query):
		row=cursor.fetchone()
	try: 
		password=row[0]
		if pWord==password:
			db_log(uName+" logged in")			
			return "true"
		else:
			db_log("User failed to log in")				
			return "false"
	#56-58: If a username doesn't exist in the database, you get a type error if you try to put row[0] in a variable.	
	except TypeError:
		db_log("User failed to log in")			
		return "false"

#62-79: addUser function adds a user's credentials into the database
def addUser(username, password, fName, lName):
	#64-67: Gets a count of the rows and adds one in order to create a primary key for the table
	query1="SELECT COUNT(*) FROM accounts"
	with cursor.execute(query1):
		row=cursor.fetchone()
	count=row[0]+1
	
	#70-79: Inserts the user's row into the database
	query2="INSERT INTO accounts VALUES ("+str(count)+",'"+username+"','"+password+"','"+fName+"','"+lName+"','',0,0,0,0,0,0,0,',,',',,')"
	try:
		cursor.execute(query2)
		connection.commit()
		db_log("User "+username+" was created")			
		return "true"
	#77-79: If a username is already taken, it gives an intergrity error
	except pyodbc.IntegrityError:		
		db_log("Failed to create new user")			
		return "false"

#82-96: addScores adds a user's scores to their account
def addScores(user, timeTrav, songLis, country, edm, hiphop, pop, rock):
	#84-90: Puts the new values into a dictionary to iterate through with the Select statement	
	new=[int(timeTrav),int(songLis),int(country),int(edm),int(hiphop),int(pop),int(rock)]	
	query1="SELECT timeTraveled, songsListenedTo, country, edm, hiphop, pop, rock FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#89-90: Adds the old scores with the new scores to put them back into the table		
		for i in range(len(row)):
			new[i]=new[i]+row[i]
	#92-96: Updates the row with the new scores and commits them
	query2="UPDATE accounts SET timeTraveled="+str(new[0])+", songsListenedTo="+str(new[1])+", country="+str(new[2])+", edm="+str(new[3])+", hiphop="+str(new[4])+", pop="+str(new[5])+", rock="+str(new[6])+" WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("New scores added to "+user)	
	return "true"

#99-111: showScores sends the user's score values to the Front End
def showScores(user):
	resp=''	
	#102-111: Query gets the values from the user's account
	query1="SELECT timeTraveled, songsListenedTo, country, edm, hiphop, pop, rock FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		#106-107: Adds the scores into a string seperated by commas	
		for i in row:
			resp=resp+","+str(i)
	#109-111:Adds the username to the string and returns the whole string	
	resp=user+resp
	db_log("User "+user+" checked their scores")		
	return resp

#114-151: addFriend takes two usernames and updates the database to add each of those users in their friends column
def addFriend(user, friend):
	#116-130: Fetches the current friends list and userID of both the user and the friend they want to add.	
	query1="SELECT friends, userID FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currFriends1=str(row[0])	
		useID1=str(row[1])
	query2="SELECT friends, userID FROM accounts WHERE username='"+friend+"'"
	with cursor.execute(query2):
		row=cursor.fetchone()
		#125-130: If the username put in does not exist, we get a TypeError		
		try:		
			currFriends2=str(row[0])	
			useID2=str(row[1])
		except TypeError:
			db_log("User "+user+" failed to add friend")	
			return "false"
	#131-142: First checks if the friends are already added. Then adds the userID to each person's friends list
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
	#144-151: Updates the accounts with the new friends list
	query3="UPDATE accounts SET friends='"+newFriends1+"' WHERE username='"+user+"'"
	cursor.execute(query3)
	connection.commit()
	query4="UPDATE accounts SET friends='"+newFriends2+"' WHERE username='"+friend+"'"
	cursor.execute(query4)
	connection.commit()
	db_log("User "+user+" added new friend "+friend)	
	return "true"

#154-179: showFriends gives the usernames of a person's friends
def showFriends(user):
	#156-160: Gets the friends string from the account and convert it into a list
	query1="SELECT friends FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		friends=str(row[0])
	friendList=friends.split(',')
	#162-170: Iterates through the list to get the usernames and put them into the old list
	try:	
		for i in range(len(friendList)):
			query="SELECT username FROM accounts WHERE userID='"+friendList[i]+"'"
			with cursor.execute(query):
				row=cursor.fetchone()
				friendList[i]=str(row[0])
	except TypeError:
		db_log("User "+user+" checked his friends list")		
		return 'No friends'
	#172-179: Iterates though the list again to put the values into a string to send to the front end
	friendsShow=''	
	for i in range(len(friendList)):
		if friendsShow=='':
			friendsShow=friendList[i]
		else:
			friendsShow=friendsShow+","+friendList[i]
	db_log("User "+user+" checked his friends list")
	return friendsShow

#182-199: saveRoute takes the time of a user's favorite route and replaces the old one he first put in with the new one
def saveRoute(user, route):
   	#184-192: Fetches the current faveRoute list and adds the new route to it and takes out the oldest		
	query1="SELECT faveRoute FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currRoutes=row[0]
	currRoutes=currRoutes.split(',')
	
	currRoutes[0]=currRoutes[1]
	currRoutes[1]=currRoutes[2]
	currRoutes[2]=route
	#194-199: Puts the newRoute list into the accounts table
	newRoute=currRoutes[0]+","+currRoutes[1]+","+currRoutes[2]
	query2="UPDATE accounts SET faveRoute='"+newRoute+"' WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("User "+user+" saved a new route")	
	return "true"

#202-208: showRoutes displays the routes for a specific user
def showRoutes(user):
	#204-208: Selects the routes from the DB and sends it back
	query1="SELECT faveRoute FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
	db_log("User "+user+" checked his routes")	
	return row[0]

#211-217: showPlaylists displays the playists for a specific user
def showPlaylists(user):
	#213-217: Selects the playlists from the DB and sends it back
	query1="SELECT favePlaylist FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
	db_log("User "+user+" checked his playlists")	
	return row[0]

#220-237: savePlaylist takes the ID of a user's favorite playlist and replaces the old one he first put in with the new one
def savePlaylist(user, playlist):
	#222-230: Fetches the current favePlaylist list and adds the new playlist to it and takes out the oldest		
	query1="SELECT favePlaylist FROM accounts WHERE username='"+user+"'"
	with cursor.execute(query1):
		row=cursor.fetchone()
		currPlaylists=row[0]
	currPlaylists=currPlaylists.split(',')
	
	currPlaylists[0]=currPlaylists[1]
	currPlaylists[1]=currPlaylists[2]
	currPlaylists[2]=playlist
	#232-237: Puts the newPlaylists list into the accounts table
	newPlaylists=currPlaylists[0]+","+currPlaylists[1]+","+currPlaylists[2]
	query2="UPDATE accounts SET favePlaylist='"+newPlaylists+"' WHERE username='"+user+"'"
	cursor.execute(query2)
	connection.commit()
	db_log("User "+user+" saved a new playlist")	
	return "true"

#240-253: showMessages shows all the messages a user has ever received
def showMessages(user):
	#242-253: Selects the users who sent the messages and the messages for a specific user
	query1="SELECT toUser, fromUser, body FROM messages WHERE toUser='"+user+"' OR fromUser='"+user+"'"
	resp=''	
	with cursor.execute(query1):
		row=cursor.fetchone()
		#247-251: Adds the users and messages into a string that the Front End will receive				
		if row==None:
			return "No messages"		
		while row:
			resp=resp+"FROM "+str(row[1])+": "+row[2]+" TO "+row[0]+"ENDMESSAGE"
			row=cursor.fetchone()
	db_log("User "+user+" checked his messages")		
	return resp

#256-280: sendMessage sends a message to a user, simple enough
def sendMessage(fromUser, toUser, message):
	#258-260: Makes sure the user does not send a message to nobody
	if toUser=="":
		db_log("User "+fromUser+" failed to send a message")			
		return "false"
	else:	
		#263-273: Checks to see if the username entered exists
		users=''	
		query1="SELECT username FROM accounts"
		with cursor.execute(query1):
			row=cursor.fetchone()
			while row:
				users=users+row[0]+","
				row=cursor.fetchone()
		users=users.split(",")	
		if toUser not in users:
			db_log("User "+fromUser+" failed to send a message")			
			return "false"
		else:
			#276-280: Enters the message into the database
			query2="INSERT INTO messages (toUser, fromUser, body) VALUES (\'"+toUser+"\',\'"+fromUser+"\',\'"+message+"\')"
			cursor.execute(query2)
			connection.commit()
			db_log("User "+fromUser+" sent a message to "+toUser)			
			return 'true'
