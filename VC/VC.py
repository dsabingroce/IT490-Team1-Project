#!/usr/bin/python

import pika
import os
import shutil


cred=pika.PlainCredentials('RMQ', 'RMQ_1234')

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))
channel = connection.channel()

channel.queue_declare(queue='VC_pull', durable=True)
channel.queue_declare(queue='VC_rollback', durable=True)
channel.queue_declare(queue='VC_push', durable=True)

################# PULL FUNCTION #####################

def pull(ch, method, props, body):
	items = body.split(',')	
	user = items[0]
	dest = items[1]
	most_recent = 0
	for version in os.listdir('/home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/' + user + "/"):
		if int(version) > most_recent:
			most_recent = int(version)
	
	hostname = dest.split(":")[0]
	path = dest.split(":")[1]
	
	copycmd = "ssh " + hostname + " 'rm -rf " + path + "*' && scp -r -i ~/.ssh/id_rsa /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent) + "/* " + dest 
	
	#copycmd = "cp -rf /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent) + "/* /mnt/" + user + "/" 
	os.system(copycmd)
	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	print("Pull from: " + user)
	
################# ROLLBACK FUNCTION #####################
	
def rollback(ch, method, props, body):			
	items = body.split(',')
	user = items[0]
	dest = items[1]
	choice = items[2]
	
	most_recent = int(choice)
	
	if choice == "previous":
		most_recent = 0
		for version in os.listdir('/home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/' + user):
			if int(version) > most_recent:
				most_recent = int(version) - 1
	
	hostname = dest.split(":")[0]
	path = dest.split(":")[1]
	
	copycmd = "ssh " + hostname + " 'rm -rf " + path + "*' && scp -r -i ~/.ssh/id_rsa /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent) + "/* " + dest 
	os.system(copycmd)
	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	print("User, " + user + ", rollbacked to version " + str(most_recent))

################# PUSH FUNCTION #####################
	
def push(ch, method, props, body):
	items = body.split(',')	
	user = items[0]
	dest = items[1]
	most_recent = 0
	for version in os.listdir('/home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/' + user):
		if int(version) > most_recent:
			most_recent = int(version)
	
	copycmd = "mkdir /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent + 1) + " && scp -r -i ~/.ssh/id_rsa " + dest + "* /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent + 1) + "/"
	
	#copycmd = "mkdir /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent + 1) + " & cp -rf /mnt/" + user + "/* /home/mara/IT490_Dev/IT490-Team1-Project/VersionControl/versions/" + user + "/" + str(most_recent + 1) 
	os.system(copycmd)
	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='VC_push', on_message_callback=push)
channel.basic_consume(queue='VC_rollback', on_message_callback=rollback)
channel.basic_consume(queue='VC_pull', on_message_callback=pull)
	
channel.start_consuming()
