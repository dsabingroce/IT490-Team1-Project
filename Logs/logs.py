#!/usr/bin/env python
import pika
import time

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
	
