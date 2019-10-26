# IT490-Team1-Project Travel Tune

## Project Overview
Travel Tune is a application.

## Components
This project is comprised of four separate servers that are connected to a single network adapter via ethernet. Below is a breakdown of these four servers.

### RabbitMQ Server (RMQ)
This server's primary function is to function as the message broker or "middleman" between all the other servers. This means, that this server recieves, controls, and organizes all communications between the other three servers. This is all done through a package called RabbitMQ, which handles JSON and AMQP messages. It reads metadata tied to these messages and places them in appropriate queues. These queues line up messages for the servers that are listening on them (consumers). The servers sending these messages (publishers) can also use an RPC protocol to send messages and then await a response.   

#### RPC Messaging Structure
Remote Procedure Calls (RPCs) are a method of communication between machines that involve a request message followed by a response message in the opposite direction. This structure is accomplished by adding a "reply_to" and correlation id to the AMQP message itself. When a server recieves a message from a client, it processes information for its response. It sends this message to the "reply_to" queue that the client is listening on as it waits. The correlation id is to help the client distiguish what request this response is related to.      

### Database
The database code, which can be found in the "Database" folder, is written in Python, and uses several modules to communicate to and from the RMQ server and perform queries to the MySQL database. 

#### Queries
<The types of queries involved>

### DMZ
The DMZ's purpose in this structure is to be the application's gateway to the internet. If the other servers were capable to connecting to the internet by themselves, that could be seen as a touchpoint or vulnerablilty. 

#### API Calls
<The APIs this app uses>

### Front End Web Server
This component for the application serves as the user interface. The front end is used to take input from the user and use it to send off requests to the other servers. That information is then received and presented back to the user. 

#### Pages
<The pages and wireframe of the site>

