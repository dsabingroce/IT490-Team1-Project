#!/usr/bin/env python
import pika
import sys
import socket
import fcntl
import struct

#Bullshit because getting the IP of a VM is wonky
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

#IMPORTANT: Insert ethernet adapter device name here
ip = get_ip_address('enp0s3')

cred = pika.PlainCredentials('RMQ','RMQ_1234')

user = "RMQ"
dest = 'mara@' + ip + ':/home/mara/RMQ/'

print(ip)

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()


if len(sys.argv) > 1:
	if sys.argv[1] == 'pull':
		lit_exchange = "VC_pull"
		message = user + "," + dest
	elif sys.argv[1] == 'push':
		lit_exchange = "VC_push"
		message = user + "," + dest
	elif sys.argv[1] == 'rollback':
		lit_exchange = "VC_rollback"
		if len(sys.argv) >= 3:
			version = sys.argv[2]
		else:
			version = "previous"
		message = user + ',' + dest + ',' + version
	else:
		print("Argument Options: 'pull', 'push', 'rollback [version number]'")
		exit()
		
	channel.exchange_declare(exchange=lit_exchange, exchange_type='direct', durable=True)
	channel.basic_publish(exchange=lit_exchange, routing_key='', body=message)

		
else:
	print("Argument Options: 'pull', 'push', 'rollback [version number]'")
	exit()

connection.close()
