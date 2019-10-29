<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Main Menu</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
   
        <div class="Square">

        <center><h1>Menu page</h1>
		<h2>What would you like to do?</h2>
            <form action ="Registration.php" method="post">
                
		<br>
                
                <input type="button" onclick="location.href='select_route.php';"value='Create new playlist' />
		<input type="button" onclick="location.href='saved_playlist.php';"value='Go to saved playlist' />
		<input type="button" onclick="location.href='social.php';"value='Go to social' />
		<input type="button" onclick="location.href='score_board.php';"value='Go to scoreboard' />
		<br><br>
		<input type="button" onclick="location.href='index.html';"value='Log out' />

            </form>
        </center>
       
    </div>
</main>
</body>
</html>
