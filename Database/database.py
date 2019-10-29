#2-3: Imports all the functions and pika client to connect to RabbitMQ
from functions import *
import pika

#5-9: Puts in credentials and connects to RabbitMQ
cred=pika.PlainCredentials('DB', 'DB_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()

#12-23: Each queue declared represents a different function the database runs after receiving information
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

#26: Keeps tracks of the user logged in currently
user=''

#29-40: Takes the username,password and sends the user true or false if they are verified
def auth_request(ch, method, props, body):			
	username = body.split(',')[0]
	password = body.split(',')[1]
	print ("User="+username+" Password="+password)
	response = auth(username, password)
	print response
	#36-38: If the user if verified, stores their username	
	if response=='true':
		global user
		user=username
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#43-52: Takes the username, password, first name, and last name to add an account
def add_request(ch, method, props, body):
	uName = body.split(',')[0]
	pWord = body.split(',')[1]
	fName = body.split(',')[2]
	lName = body.split(',')[3]
	print ("User="+uName+" Password="+pWord+" Firstname="+fName+" Lastname="+lName)
	response = addUser(uName, pWord, fName, lName)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#55-67: Takes all the scoreable variables and adds them to a user's account
def addScores_request(ch, method, props, body):
	global user	
	timeTrav = body.split(',')[0]
	songLis = body.split(',')[1]
	country = body.split(',')[2]
	edm = body.split(',')[3]
	hiphop = body.split(',')[4]
	pop = body.split(',')[5]
	rock = body.split(',')[6]
	print (body.split(','))
	response = addScores(user, timeTrav, songLis, country, edm, hiphop, pop, rock)
	print response
	ch.basic_ack(delivery_tag=method.delivery_tag)

#70-76: Sends the user's scores to the FE
def showScores_request(ch, method, props, body):
	global user	
	print body
	response = showScores(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#79-85: Takes a username and adds that username's ID to a user's friendlist
def addFriend_request(ch, method, props, body):
	global user	
	print body
	response = addFriend(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#88-94: Sends the user's friends to the FE
def showFriends_request(ch, method, props, body):
	global user	
	print body
	response = showFriends(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#97-102: Takes a route length and saves it for a user
def saveRoute_request(ch, method, props, body):
	global user	
	print body
	response = saveRoute(user, body)
	print response
	ch.basic_ack(delivery_tag=method.delivery_tag)

#105-110: Takes a playlist link and saves it to the user's account
def savePlaylist_request(ch, method, props, body):
	global user	
	print body
	response = savePlaylist(user, body)
	print response
	ch.basic_ack(delivery_tag=method.delivery_tag)

#113-119: Sends all the messages a user has send and received to the front end.
def showMessages_request(ch, method, props, body):
	global user	
	print body
	response = showMessages(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#122-129: Saves a message for a user to see when they log in
def sendMessage_request(ch, method, props, body):
	global user	
	print body
	body=body.split("STARTOFMESSAGE")
	response = sendMessage(user, body[0], body[1])
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#132-138: Sends the FE all the routes a user has saved
def showRoutes_request(ch, method, props, body):
	global user	
	print body
	response = showRoutes(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#141-147: Sends the FE all the playlists a user has saved
def showPlaylists_request(ch, method, props, body):
	global user	
	print body
	response = showPlaylists(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

#150-166: Begins to listen on each queue and logs that the server has started.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DB_auth', on_message_callback=auth_request)
channel.basic_consume(queue='DB_add', on_message_callback=add_request)
channel.basic_consume(queue='DB_addScores', on_message_callback=addScores_request)
channel.basic_consume(queue='DB_showScores', on_message_callback=showScores_request)
channel.basic_consume(queue='DB_addFriend', on_message_callback=addFriend_request)
channel.basic_consume(queue='DB_showFriends', on_message_callback=showFriends_request)
channel.basic_consume(queue='DB_saveRoute', on_message_callback=saveRoute_request)
channel.basic_consume(queue='DB_savePlaylist', on_message_callback=savePlaylist_request)
channel.basic_consume(queue='DB_showMessages', on_message_callback=showMessages_request)
channel.basic_consume(queue='DB_sendMessage', on_message_callback=sendMessage_request)
channel.basic_consume(queue='DB_showRoutes', on_message_callback=showRoutes_request)
channel.basic_consume(queue='DB_showPlaylists', on_message_callback=showPlaylists_request)
	
print(' [x] Awaiting Authentication RPC requsts')
db_log("Database server started")
channel.start_consuming()
