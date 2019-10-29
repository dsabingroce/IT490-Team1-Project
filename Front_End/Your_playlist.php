<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Your Playlist</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
    <div class="Square">

        <center><h1>Your Playlist: </h1>



<?php
	$saved_playlist_box = $_POST['saved_playlist_box'];
	$name_of_playlist = $_POST['name_of_playlist'];
	
/*
	$genre_country = $_POST['country'];
	$genre_hip_hop = $_POST['hip-hop'];
	$genre_pop = $_POST['pop'];
	$genre_edm = $_POST['edm'];
	$genre_rock = $_POST['rock'];

if ($genre_country){
    $music_type = "country";
}
elseif($genre_hip_hop){
	$music_type= "hip-hop";
}
elseif($genre_pop){
	$music_type= "pop";
}
elseif($genre_edm){
	$music_type= "edm";
}
elseif($genre_rock){
	$music_type= "rock";
}
else{
	$music_type= "hip-hop";
}
*/

 
 $music_type=$_POST ['genre_selection']; 

$genre_check = ('curl -o seed.json -X "GET" "https://api.spotify.com/v1/recommendations?limit=3&market=US&seed_genres='.$music_type.'" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer BQAJOm4rnh-AQA6FSYVQDOp4yz2R0vx1vk_buPemDsiYkD-eHh25luMIaVqXNuVm0jb2x_aRkU03p5DPILpoxgXwuasZbf7mdTtRByyKtQ5OYdMotbskXvN30dndCp3TJjjRU5-eisdbHXfDpFoZpQGYwLMOLizRIHWAaqYPzqBDPxU"');





############################################################################


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
            "DMZ_genre",
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

	public function one_way($message) {
		$this->channel->exchange_declare('DB_savePlaylist', 'direct', false, true, false);	
		$msg = new AMQPMessage($message);
		$this->channel->basic_publish($msg, 'DB_savePlaylist');
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
        $this->channel->basic_publish($msg, '', 'DMZ_genre');
        
	while (!$this->response) {
            $this->channel->wait();
        }
		return ($this->response);
	
        return ($this->test);
    }
}

$rpc = new RpcClient();
#$response = $rpc->call("$genre_check");
$response = $rpc->call("$music_type,$name_of_playlist");

if ($saved_playlist_box == "true") {
	#echo "sending playlist to DB";
	$rpc->one_way("$response");	
}

echo "Please visit the url:   ";
echo $response;


 



?>

<br>
<br>
<br>
     
<br>
<br>
<br>

<input type="button" onclick="location.href='main_menu.php';"value='main menu' />
	
</div>
</main>
</body>
</html>
