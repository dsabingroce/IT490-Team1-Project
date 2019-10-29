<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Social</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
  <div class="Square">


<body>



<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;


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
            "DB_showFriends",
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
        $this->channel->basic_publish($msg, '', "DB_showFriends");
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}

$rpc = new RpcClient();
$response = $rpc->call("");
#echo $response, "\n";

?>


    
<font color = "#0000cd"><h1>Social</h1></font>
    
        
	<form action ="add_friend.php" action="/" method="post">
      <!--  <h3 align="left">Add friend: </h3> -->
	<table>
	    <tr>
		<h3 align="left">Current friends: 
		
<?php 

	if($_GET['status'] == "false"){
		echo '<pre>';
		echo "Invalid username. Please try again.\n";
		echo "Current friends: "."$response";
		echo '</pre>';
	}
	else{
 		echo $response; 
	} 
?>
</h3>

	     </tr>
		<br>
		<br>
		<br>
            <tr>
	
                <td><h3 align="left">Add friend: </h3></td>
		<td><input type="text" name="addFriend" id="addFriend"></td>
		<td><input align="right" type="submit" value='enter'></td>
	</form>

	 </tr>
	
	</table>


	<br>
	<br>

        <input type="button" onclick="location.href='main_menu.php';"value='Return to Main Menu' />
<input type="button" onclick="location.href='view_messages.php';"value='View & Send Messages' />
		</td> 
		
            </tr> 
	
        </table>
    </form>
</body>



</main>
</body>
</html>
