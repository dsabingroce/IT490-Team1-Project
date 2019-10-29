<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Route Selection</title>
    <link rel="stylesheet" href="login.css">
</head>

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
            "DB_showRoutes",
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
        $this->channel->basic_publish($msg, '', "DB_showRoutes");
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}

$rpc = new RpcClient();
$response = $rpc->call("");
//echo $response;

$saved_routes = explode(",", $response); 

?>

<body>
<main>
 
        <div class="Square">

        <center><h1>Select route</h1>
		<h2>Choose one of the following.</h2>
            <form action ="Registration.php" method="post">
                
		<br>
		<?php                
		$count_route = 0;
		foreach ($saved_routes as $route) {
			if ($route != "") {
				$count_route = $count_route + 1;
				$saved_time = gmdate("H:i:s", $route);
				echo "<input type=\"button\" onclick=\"location.href='playlist.php?time=$route';\" value='Use Route $count_route: $saved_time minutes' />";
			}
		}
        ?>
      	<br>
		<br>
		<input type="button" onclick="location.href='new_route.php'; "value='Create a new route' />

<!--

		<input type="button" onclick="location.href='saved_route.php';" value='Use saved route 1' />
		<input type="button" onclick="location.href='saved_route.php';" value='Use saved route 2' />
		<input type="button" onclick="location.href='saved_route.php';" value='Use saved route 3' />
-->
		<br><br>
		<input type="button" onclick="location.href='main_menu.php';"value='Return to main menu' />
		
            </form>
        </center>

    </div>
</main>
</body>
</html>
