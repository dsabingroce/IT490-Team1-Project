<?php
include "logs.php";
log_db("User creates a new account.");

?>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration</title>
    <link rel="stylesheet" href="style.css">

</head>
<body>
<div class="square">

<?php


require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;


$fname = $_POST['firstName'];
$lname = $_POST['lastName'];
$username = $_POST['username'];


$pass = $_POST['password'];


/*
$flag = true;
if ($flag){
    $flag = true;
    if (empty($fname)){
        echo " First Name field is empty<br>";
        $flag = false;
    }

    if (empty($lname)){
        echo " Last Name field is empty<br>";
        $flag = false;
    }

    if (empty($username)) {
        echo "User Name field is empty<br>";
        $flag = false;}
   /* elseif (strpos($email, '@') === false) {
        echo("Email is not valid, missing @ symbol. <br>");
        $flag = false;} 
    
    if ((strlen($pass)==0)) {
        echo("Password field is empty<br>");
        $flag = false;
    } else if(strlen($pass) <8) {
        echo("password needs to be 8 characters or more<br>");
        $flag = false;
    }

    return $flag;
}
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
            "DB_add",
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
        $this->channel->basic_publish($msg, '', 'DB_add');
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}

$rpc = new RpcClient();
$response = $rpc->call("$username,$pass,$fname,$lname");
echo $response;
if ($response == "true"){
    header("Location: index.html");
	
}

?>


</div>
</body>
</html>
