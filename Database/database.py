from functions import *
import pika

cred=pika.PlainCredentials('DB', 'DB_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()


channel.queue_declare(queue='DB_auth', durable=True)
channel.queue_declare(queue='DB_add', durable=True)
channel.queue_declare(queue='DB_addScores', durable=True)
channel.queue_declare(queue='DB_showScores', durable=True)
channel.queue_declare(queue='DB_addFriend', durable=True)
channel.queue_declare(queue='DB_showFriends', durable=True)
channel.queue_declare(queue='DB_saveRoute', durable=True)
channel.queue_declare(queue='DB_selectRoute', durable=True)
channel.queue_declare(queue='DB_savePlaylist', durable=True)
channel.queue_declare(queue='DB_selectPlaylist', durable=True)

user='test1'

def auth_request(ch, method, props, body):
	global user	
	username = body.split(',')[0]
	password = body.split(',')[1]
	print ("User="+username+" Password="+password)
	response = auth(username, password)
	print response
	if response=='true':
		user=username
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def add_request(ch, method, props, body):
	uName = body.split(',')[0]
	pWord = body.split(',')[1]
	fName = body.split(',')[2]
	lName = body.split(',')[3]
	print ("User="+uName+" Password="+pWord+" Firstname="+fName+" Lastname="+lName)
	response = addUser(username, password, fName, lName)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def addScores_request(ch, method, props, body):
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
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def showScores_request(ch, method, props, body):
	print body
	response = showScores(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def addFriend_request(ch, method, props, body):
	print body
	response = addFriend(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def showFriends_request(ch, method, props, body):
	print body
	response = showFriends(user)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def saveRoute_request(ch, method, props, body):
	print body
	response = saveRoute(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def selectRoute_request(ch, method, props, body):
	print body
	response = selectRoute(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def savePlaylist_request(ch, method, props, body):
	print body
	response = savePlaylist(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

def selectPlaylist_request(ch, method, props, body):
	print body
	response = selectPlaylist(user, body)
	print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DB_auth', on_message_callback=auth_request)
channel.basic_consume(queue='DB_add', on_message_callback=add_request)
channel.basic_consume(queue='DB_addScores', on_message_callback=addScores_request)
channel.basic_consume(queue='DB_showScores', on_message_callback=showScores_request)
channel.basic_consume(queue='DB_addFriend', on_message_callback=addFriend_request)
channel.basic_consume(queue='DB_showFriends', on_message_callback=showFriends_request)
channel.basic_consume(queue='DB_saveRoute', on_message_callback=saveRoute_request)
channel.basic_consume(queue='DB_selectRoute', on_message_callback=selectRoute_request)
channel.basic_consume(queue='DB_savePlaylist', on_message_callback=savePlaylist_request)
channel.basic_consume(queue='DB_selectPlaylist', on_message_callback=selectPlaylist_request)
	
print(' [x] Awaiting Authentication RPC requsts')
channel.start_consuming()
