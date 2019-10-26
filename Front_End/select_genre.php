<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>chose genre</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
    <div class="Square">


        <?php

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



$rpc = new RpcClient();
$response = $rpc->call("$location");

#echo $response;
echo "You will arrive in: " .$response. " seconds.";



?>

	<center>
            <h1>Next: Select Genre</h1>
            <form action ="Playlist.php" method="post">

                <table>
                    <tr>
                        <td>Country:</td>
                        <td><input type="checkbox" name="country" id="Country_music" name="Country"></td>
                    </tr>
                    <tr>
                        <td>Hip Hop:</td>
                        <td><input type="checkbox" name="hip-hop" id="Hip_Hop_music" name="Hip Hop"></td>
                    </tr>
                    <tr>
                        <td>Techno</td>
			<td><input type="checkbox" name="techno" id="Techno_music" name="Techno"></td>
                    </tr>

		<tr>
                        <td>Rock</td>
			<td><input type="checkbox" id="Rock_music" name="rock" name="Rock"></td>
                    </tr>


                </table>
                <input type="submit" name="submit" value="submit">
                <input type="button" onclick="location.href='new_route.html';"value='back' />

            </form>
        </center> -->
    </div>





<?php


	$check_genre = $_POST['country'];

	#$check_genre = country;
if ($check_genre){
    $check_genre = "country";
    }

$genre_check = ('curl -o seed.json -X "GET" "https://api.spotify.com/v1/recommendations?limit=3&market=US&seed_genres='.$check_genre.'" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer BQC9kkxcMKi9aVVvr8RX6p7Q_AgY0TUZjueWp4YWclwUVEYXkh-eUKL03lUaLmvWIxXA6XOBmKL2DCHvlW5Lcl9h-rzs3ntGt2h2ts41Gpo4mGodl1ZCVC5CCKXjwL9QRY-wNCAIqhiNqf8QUNaBAsOvvlGevEW_B8BW7gBLuHmmRtk"');

$rpc = new RpcClient();
$response = $rpc->call("$genre_check");

echo $response;
#echo "You will arrive in: " .$response. " seconds.";


?>

</main>
</body>
</html>
