#2-3: Imports all the functions and pika client to connect to RabbitMQ
from backup_functions import *
import pika

#5-9: Puts in credentials and connects to RabbitMQ
cred=pika.PlainCredentials('DB', 'DB_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()

#12-23: Each queue declared represents a different function the database runs after receiving information
channel.queue_declare(queue='DBB_auth', durable=True)
channel.queue_declare(queue='DBB_add', durable=True)
channel.queue_declare(queue='DBB_addScores', durable=True)
channel.queue_declare(queue='DBB_showScores', durable=True)
channel.queue_declare(queue='DBB_addFriend', durable=True)
channel.queue_declare(queue='DBB_showFriends', durable=True)
channel.queue_declare(queue='DBB_saveRoute', durable=True)
channel.queue_declare(queue='DBB_savePlaylist', durable=True)
channel.queue_declare(queue='DBB_showMessages', durable=True)
channel.queue_declare(queue='DBB_sendMessage', durable=True)
channel.queue_declare(queue='DBB_showRoutes', durable=True)
channel.queue_declare(queue='DBB_showPlaylists', durable=True)
channel.queue_declare(queue='DBB_sharePlaylist', durable=True)
channel.queue_declare(queue='DBB_backup', durable=True)
channel.queue_declare(queue='DB_auth', durable=True)
channel.queue_declare(queue='DB_add', durable=True)
channel.queue_declare(queue='DB_addScores', durable=True)
channel.queue_declare(queue='DB_showScores', durable=True)
channel.queue_declare(queue='DB_addFriend', durable=True)
channel.queue_declare(queue='DB_showFriends', durable=True)
channel.queue_declare(queue='DB_saveRoute', durable=True)
channel.queue_declare(queue='DB_savePlaylist', durable=True)
channel.queue_declare(queue='DB_showMessages', durable=True)
channel.queue_declare(queue='DB_sendMessage', durable=True)
channel.queue_declare(queue='DB_showRoutes', durable=True)
channel.queue_declare(queue='DB_showPlaylists', durable=True)
channel.queue_declare(queue='DB_sharePlaylist', durable=True)
channel.queue_declare(queue='DB_ping', durable=True)

#26: Keeps tracks of the user logged in currently
user=''
disaster=False
recovery=""

#29-38: Takes the username,password and sends the user true or false if they are verified
def auth_request(ch, method, props, body):			
	username = body.split(',')[0]
	password = body.split(',')[1]
	response = auth_DBB(username, password)
	#36-38: If the user if verified, stores their username	
	if response=='true':
		global user
		user=username
	if disaster==True:
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#41-48: Takes the username, password, first name, and last name to add an account
def add_request(ch, method, props, body):
	uName = body.split(',')[0]
	pWord = body.split(',')[1]
	fName = body.split(',')[2]
	lName = body.split(',')[3]
	response = addUser_DBB(uName, pWord, fName, lName, disaster)
	if disaster==True:
		global recovery
		if response=="false":
			ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
		else:
			recovery=recovery+"END"+response.split("END")[1]
			ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response.split("END")[0]))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#51-61: Takes all the scoreable variables and adds them to a user's account
def addScores_request(ch, method, props, body):
	global user	
	timeTrav = body.split(',')[0]
	songLis = body.split(',')[1]
	country = body.split(',')[2]
	edm = body.split(',')[3]
	hiphop = body.split(',')[4]
	pop = body.split(',')[5]
	rock = body.split(',')[6]
	response = addScores_DBB(user, timeTrav, songLis, country, edm, hiphop, pop, rock)
	if disaster==True:
		global recovery
		recovery=recovery+","+response
	ch.basic_ack(delivery_tag=method.delivery_tag)

#64-68: Sends the user's scores to the FE
def showScores_request(ch, method, props, body):
	global user	
	response = showScores_DBB(user)
	if disaster==True:	
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#71-75: Takes a username and adds that username's ID to a user's friendlist
def addFriend_request(ch, method, props, body):
	global user	
	response = addFriend_DBB(user, body)
	if disaster==True:		
		ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response.split(",")[0]))
		global recovery
		recovery=recovery+","+response.split(",")[1]+","+response.split(",")[2]
	ch.basic_ack(delivery_tag=method.delivery_tag)

#78-82: Sends the user's friends to the FE
def showFriends_request(ch, method, props, body):
	global user	
	response = showFriends(user)
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#85-88: Takes a route length and saves it for a user
def saveRoute_request(ch, method, props, body):
	global user	
	response = saveRoute(user, body)
	ch.basic_ack(delivery_tag=method.delivery_tag)

#91-94: Takes a playlist link and saves it to the user's account
def savePlaylist_request(ch, method, props, body):
	global user	
	response = savePlaylist(user, body)
	ch.basic_ack(delivery_tag=method.delivery_tag)

#97-101: Sends all the messages a user has send and received to the front end.
def showMessages_request(ch, method, props, body):
	global user	
	response = showMessages(user)
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#104-109: Saves a message for a user to see when they log in
def sendMessage_request(ch, method, props, body):
	global user	
	body=body.split("STARTOFMESSAGE")
	response = sendMessage(user, body[0], body[1])
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#112-116: Sends the FE all the routes a user has saved
def showRoutes_request(ch, method, props, body):
	global user	
	response = showRoutes(user)
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#119-123: Sends the FE all the playlists a user has saved
def showPlaylists_request(ch, method, props, body):
	global user	
	response = showPlaylists(user)
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def sharePlaylist_request(ch, method, props, body):
	global user
	body=body.split(",")
	reponse=sendMessage(user, body[0], body[1])
	ch.basic_ack(delivery_tag=method.delivery_tag)

def ack(ch, method, props, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)

def backup_request(ch, method, props, body):
	global disaster	
	global recovery
	if body=="true":
		disaster=True
		channel.basic_consume(queue='DB_auth', on_message_callback=ack, consumer_tag='DB_auth')
		channel.basic_consume(queue='DB_add', on_message_callback=ack, consumer_tag='DB_add')
		channel.basic_consume(queue='DB_addScores', on_message_callback=ack, consumer_tag='DB_addScores')
		channel.basic_consume(queue='DB_showScores', on_message_callback=ack, consumer_tag='DB_showScores')
		channel.basic_consume(queue='DB_addFriend', on_message_callback=ack, consumer_tag='DB_addFriend')
		channel.basic_consume(queue='DB_showFriends', on_message_callback=ack, consumer_tag='DB_showFriends')
		channel.basic_consume(queue='DB_saveRoute', on_message_callback=ack, consumer_tag='DB_saveRoute')
		channel.basic_consume(queue='DB_savePlaylist', on_message_callback=ack, consumer_tag='DB_savePlaylist')
		channel.basic_consume(queue='DB_showMessages', on_message_callback=ack, consumer_tag='DB_showMessages')
		channel.basic_consume(queue='DB_sendMessage', on_message_callback=ack, consumer_tag='DB_sendMessage')
		channel.basic_consume(queue='DB_showRoutes', on_message_callback=ack, consumer_tag='DB_showRoutes')
		channel.basic_consume(queue='DB_showPlaylists', on_message_callback=ack, consumer_tag='DB_showPlaylists')
		channel.basic_consume(queue='DB_sharePlaylist', on_message_callback=ack, consumer_tag='DB_sharePlaylist')
		channel.basic_consume(queue='DB_ping', on_message_callback=ack, consumer_tag='DB_ping')
		recovery=""
		db_log("Database failed, starting disaster mode")
	else:	
		disaster=False
		channel.basic_cancel(consumer_tag='DB_auth')
		channel.basic_cancel(consumer_tag='DB_add')
		channel.basic_cancel(consumer_tag='DB_addScores')
		channel.basic_cancel(consumer_tag='DB_showScores')
		channel.basic_cancel(consumer_tag='DB_addFriend')
		channel.basic_cancel(consumer_tag='DB_showFriends')
		channel.basic_cancel(consumer_tag='DB_saveRoute')
		channel.basic_cancel(consumer_tag='DB_savePlaylist')
		channel.basic_cancel(consumer_tag='DB_showMessages')
		channel.basic_cancel(consumer_tag='DB_sendMessage')
		channel.basic_cancel(consumer_tag='DB_showRoutes')
		channel.basic_cancel(consumer_tag='DB_showPlaylists')
		channel.basic_cancel(consumer_tag='DB_sharePlaylist')
		channel.basic_cancel(consumer_tag='DB_ping')
		channel.basic_cancel(consumer_tag='DB_recovery')
		db_log("Database back online, forprintwarding queries")
		channel.exchange_declare(exchange='DB_recovery', exchange_type='direct', durable=True)
		channel.basic_publish(exchange='DB_recovery', routing_key='', body=recovery)
	ch.basic_ack(delivery_tag=method.delivery_tag)

#126-142: Begins to listen on each queue and logs that the server has started.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DBB_auth', on_message_callback=auth_request)
channel.basic_consume(queue='DBB_add', on_message_callback=add_request)
channel.basic_consume(queue='DBB_addScores', on_message_callback=addScores_request)
channel.basic_consume(queue='DBB_showScores', on_message_callback=showScores_request)
channel.basic_consume(queue='DBB_addFriend', on_message_callback=addFriend_request)
channel.basic_consume(queue='DBB_showFriends', on_message_callback=showFriends_request)
channel.basic_consume(queue='DBB_saveRoute', on_message_callback=saveRoute_request)
channel.basic_consume(queue='DBB_savePlaylist', on_message_callback=savePlaylist_request)
channel.basic_consume(queue='DBB_showMessages', on_message_callback=showMessages_request)
channel.basic_consume(queue='DBB_sendMessage', on_message_callback=sendMessage_request)
channel.basic_consume(queue='DBB_showRoutes', on_message_callback=showRoutes_request)
channel.basic_consume(queue='DBB_showPlaylists', on_message_callback=showPlaylists_request)
channel.basic_consume(queue='DBB_sharePlaylist', on_message_callback=sharePlaylist_request)
channel.basic_consume(queue='DBB_backup', on_message_callback=backup_request)
	
db_log("Backup database server started")
channel.start_consuming()
