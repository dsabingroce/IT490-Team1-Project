import pika
import os
import json
from pprint import pprint

script = 'curl -o new.json -d @location.json -H "Content-Type: application/json" http://www.mapquestapi.com/directions/v2/routematrix?key=8PtZTD2kqepePZgyZPkbfg7Q6EhkUvcP'

cred=pika.PlainCredentials('DMZ', 'DMZ_1234')

connection=pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))

channel = connection.channel()

channel.queue_declare(queue='DMZ_route', durable=True)


#The on request method is what the program will do when it recieves a message. 
#It grabs the information from the sender and uses it to send the response back.
def on_request(ch, method, props, body):
    print(body)
    os.system("echo "+body+" > location.json")  

    os.system(script)

    with open('new.json') as f:
    	data = json.load(f)

    time = data["time"]

    pprint(time)

    response = time

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DMZ_route', on_message_callback=on_request)

print(" [x] Awaiting Route Time Calculations RPC requests")
channel.start_consuming()
