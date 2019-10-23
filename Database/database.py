from functions import *
import pika

cred=pika.PlainCredentials('DB', 'DB_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()


channel.queue_declare(queue='DB_auth', durable=True)
channel.queue_declare(queue='DB_add', durable=True)

user=''

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

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DB_auth', on_message_callback=auth_request)
channel.basic_consume(queue='DB_add', on_message_callback=add_request)
	
print(' [x] Awaiting Authentication RPC requsts')
channel.start_consuming()
