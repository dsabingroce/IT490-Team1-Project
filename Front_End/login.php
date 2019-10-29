<?php
session_start();

include "logs.php";
log_db("User logins into Travel Tunes website.");


header('Location: main_menu.php');

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$user = $_POST['username'];
$pass = $_POST['password'];
/*
$connection = new AMQPStreamConnection('192.168.1.5', 5672, 'FE', 'FE_1234');
$channel = $connection->channel();

$channel->exchange_declare('DB', 'topic', false, true, false);

$msg = new AMQPMessage("$user,$pass");
$channel->basic_publish($msg, 'DB', 'auth');

echo "$msg->body";
*/
class RpcClient
{
    private $connection;
    private $channel;
    private $callback_queue;
    private $response;
    private $corr_id;

    public function __construct()
    {
        $this->connection = new AMQPStreamConnection(
            '192.168.1.5',
            5672,
            'FE',
            'FE_1234'
        );
        $this->channel = $this->connection->channel();
        list($this->callback_queue, ,) = $this->channel->queue_declare(
            "DB_auth",
            false,
            true,
            false,
            false
        );
        $this->channel->basic_consume(
            $this->callback_queue,
            '',
            false,
            true,
            false,
            false,
            array(
                $this,
                'onResponse'
            )
        );
    }

    public function onResponse($rep)
    {
        if ($rep->get('correlation_id') == $this->corr_id) {
            $this->response = $rep->body;
        }
    }

    public function call($n)
    {
        $this->response = null;
        $this->corr_id = uniqid();

        $msg = new AMQPMessage(
            $n,
            array(
                'correlation_id' => $this->corr_id,
                'reply_to' => $this->callback_queue
            )
        );
        $this->channel->basic_publish($msg, '', 'DB_auth');
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}

$rpc = new RpcClient();
$response = $rpc->call("$user,$pass");
echo $response;
#echo ' [.] Got ', $response, "\n";

if ($response == "true"){
	$_SESSION['logged_in'] = true;
    header("Location: main_menu.php");
}
else{
	$_SESSION['logged_in'] = false;
	header("Location: index.html");
	echo "Wrong username or password. Please try again.";
}

?>
