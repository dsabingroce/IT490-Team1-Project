# IT490-Team1-Project Travel Tune

## Project Overview


## Components
This project is comprised of four separate servers that are connected to a single network adapter via ethernet. Below is a breakdown of these four servers.

##### RabbitMQ Server (RMQ)
This server's primary function is to function as the message broker or "middleman" between all the other servers. This means, that this server recieves, controls, and organizes all communications between the other three servers. This is all done through a package called RabbitMQ, which handles JSON and AMQP messages. It reads metadata tied to these messages and places them in appropriate queues. These queues line up messages for the servers that are listening on them (consumers). The servers sending these messages (publishers) can also use an RPC protocol to send messages and then await a response.   

##### Database
The database code, which can be found in the "Database" folder, is written in Python, and uses several modules to communicate to and from the RMQ server and perform queries to the MySQL database. 

##### DMZ


##### Front End Web Server


