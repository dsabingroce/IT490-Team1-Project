<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

function log_db($message) {
	//Create timestamp for log
	$message = date('D M d H:i:s Y', strtotime("now")) . " -> " . $message; 

	//Write log to local file
	$file = './server_log';
	$current = file_get_contents($file);
	$current .= "$message\n";
	file_put_contents($file, $current);
	
	//Send message to DB for logging
	$connection = new AMQPStreamConnection('192.168.1.5', 5672, 'RMQ', 'RMQ_1234');
	$channel = $connection->channel();

	$channel->exchange_declare('DB_logs', 'direct', false, true, false);

	$msg = new AMQPMessage($message);

	$channel->basic_publish($msg, 'DB_logs');

	$channel->close();
	$connection->close();

}

?>
