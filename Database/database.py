from functions import *
import sys
import pika
import os
import subprocess

cred=pika.PlainCredentials('DB', 'DB_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()


channel.queue_declare(queue='DB_auth', durable=True)

def on_request(ch, method, props, body):
	username = body.split(',')[0]
	password = body.split(',')[1]
	print ("User="+username+" Password="+password)
	response="Here is your username: "+username+" and password: "+password
	#response = auth(username, password)
	#print response
	ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id), body=str(response))
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DB_auth', on_message_callback=on_request)
	
print(' [x] Awaiting Authentication RPC requsts')
channel.start_consuming()
