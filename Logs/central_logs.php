<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

//Determine central logging file
$log_file = "./central_log";

//Establish connections
$connection = new AMQPStreamConnection('192.168.1.5', 5672, 'RMQ', 'RMQ_1234');
$channel = $connection->channel();

//Wait for incoming messages
$channel->queue_declare('DB_logs', false, true, false, false);

echo " [*] Central Logging Enabled. Waiting for messages. To exit press CTRL+C\n";

//Callback function to write incoming messages to the central logging file
$callback = function ($msg) {
	global $log_file;
  	echo ' [x] Received ', $msg->body, "\n";
	file_put_contents($log_file, $msg->body . "\n", FILE_APPEND | LOCK_EX);
};
  
$channel->basic_consume('DB_logs', '', false, true, false, false, $callback);

while ($channel->is_consuming()) {
  	$channel->wait();
}
?>
