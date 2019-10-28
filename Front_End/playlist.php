<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Playlist</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
    <div class="Square">


        <?php

       # $email = $_POST['email'];
        $Origin_streetName = $_POST['Origin_streetName'];
        $Origin_cityName = $_POST['Origin_cityName'];
        $Origin_stateName = $_POST['Origin_stateName'];
	$Origin_zipcode = $_POST['Origin_Zipcode'];
	
	$Origin_Full = $Origin_streetName + $Origin_cityName + $Origin_stateName + $Origin_zipcode;
	
	#echo $Origin_Full;

#	echo ("{'locations':['".$Origin_streetName." ".$Origin_cityName." ".$Origin_stateName." ".$Origin_zipcode."']}");


#	echo ('{"locations":["'.$Origin_streetName.' '.$Origin_cityName.' '.$Origin_stateName.' '.$Origin_zipcode.'"]}');




#	echo " $Origin_streetName";
#       echo " $Origin_cityName";
#       echo " $Origin_stateName";
#      	echo " $Origin_zipcode";

	$Des_streetName = $_POST['Des_streetName'];
        $Des_cityName = $_POST['Des_cityName'];
        $Des_stateName = $_POST['Des_stateName'];
	$Des_zipcode = $_POST['Des_Zipcode'];

#echo $Des_streetName + " " + $Des_cityName + " " + $Des_stateName + " " + $Des_zipcode;

#	echo $Des_streetName;
#       echo $Des_cityName;
#       echo $Des_stateName;
#	echo $Des_zipcode;

$location = ('{"locations":["'.$Origin_streetName.' '.$Origin_cityName.' '.$Origin_stateName.' '.$Origin_zipcode.'","'.$Des_streetName.' '.$Des_cityName.' '.$Des_stateName.' '.$Des_zipcode.'"]}');

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
            "DMZ_route",
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
        $this->channel->basic_publish($msg, '', 'DMZ_route');
        while (!$this->response) {
            $this->channel->wait();
        }
        return ($this->response);
    }
}



##############################################################
$rpc = new RpcClient();
$response = $rpc->call("$location");

#echo $response;
$total_minutes = gmdate("H:i:s", $response);
echo "You will arrive in " .$total_minutes. " minutes.";



?>

	<center>

	<form action ="Your_playlist.php" method="post">
	<h1>Enter name of new playlist:</h1>
<input type="text" name="name_of_playlist" id="name_of_playlist" placeholder="Name the playlist">


	<table>
<!------------------------------------------------------------------>
            <h1>Select Genre</h1>
            

              <!--  <table> -->
                    <tr>
                        <td>Country:</td>
                        <td><input type="checkbox" value="true" id="country_music" name="country"></td>
                    </tr>
                    <tr>
                        <td>Hip Hop:</td>
                        <td><input type="checkbox" value="true" id="hip_hop_music" name="hip hop"></td>
                    </tr>

			<tr>
                        <td>Pop</td>
			<td><input type="checkbox" value="true" id="pop_music" name="pop"></td>
                    </tr>

                    <tr>
                        <td>EDM</td>
			<td><input type="checkbox" value="true" id="edm_music" name="edm"></td>
                    </tr>

		<tr>
                        <td>Rock</td>
			<td><input type="checkbox" value="true" id="rock_music" name="rock"></td>
                    </tr>


                </table>
                <input type="submit" name="submit" value="submit">
                <input type="button" onclick="location.href='new_route.php';"value='back' />

            </form>
        </center>
    </div>
</main>
</body>
</html>
