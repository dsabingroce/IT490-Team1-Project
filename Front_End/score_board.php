<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
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
            "DB_showScores",
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
      //  $this->channel->basic_publish($msg, '', "DB_showScores");
		$this->channel->basic_publish($msg, 'DB_showScores', "");
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}

$rpc = new RpcClient();
$response = $rpc->call("");
#echo $response;
$score_board = explode(",", $response);


?>






<font color = "#0000cd"><h1>Score Board</h1></font>
    <form action ="main_menu.php" method="post">
        
	<h3 align="left">Username: <?php echo $score_board[0] ?> </h3>


<?php $total_minutes = gmdate("H:i:s", $score_board[1]);
#echo "You will arrive in " .$total_minutes. " minutes.";

?>

        <h3 align="left">Total Time Traveled: <?php echo $total_minutes ?> </h3>

        <h3 align="left">Total number of songs listened to: <?php echo $score_board[2] ?></h3>
	<h3 align="left">Country: <?php echo $score_board[3] ?></h3>
	<h3 align="left">EDM: <?php echo $score_board[4] ?></h3>
	<h3 align="left">Hip-Hop: <?php echo $score_board[5] ?></h3>
	<h3 align="left">Pop: <?php echo $score_board[6] ?></h3>
	<h3 align="left">Rock: <?php echo $score_board[7] ?></h3>
	<br>
	<br>

        <input type="submit" name="submit" value="Main Menu"></td> 
            </tr> 
	
        </table>
    </form>
</body>




</main>
</body>
</html>
