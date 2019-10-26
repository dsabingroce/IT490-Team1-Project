import pika 
import os
import json
from pprint import pprint 

cred=pika.PlainCredentials('DMZ', 'DMZ_1234')

connection=pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))

channel = connection.channel()

channel.queue_declare(queue='DMZ_genre', durable=True)


#The on request method is what the program will do when it recieves a message. 
#It grabs the information from the sender and uses it to send the response back.
def on_request(ch, method, props, body):
    print(body)
    os.system(body)  

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DMZ_genre', on_message_callback=on_request)

print(" [x] Awaiting Route Time Calculations RPC requests")
channel.start_consuming()
