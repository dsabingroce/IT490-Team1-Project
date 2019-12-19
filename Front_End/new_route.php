<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Enter new router</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
<main>
   
        <div class="Square">

<title>Determine Time Traveled</title>

</head>
<body>
    <!--<body style="background-color: lavender"> -->
	<font color = "#0000cd"><h3>Lets begin by determining the amount of time 		you will be traveling:</h3></font>
	
	<h3>Origin</h3>

    <center><form action = "playlist.php" method="post">       
	<table>
	<!--<div style="float:left;"> -->
            <tr>
                <!--<td>Please enter Street: </td>-->
                <td><input type="text" name="Origin_streetName" placeholder="Enter Street"></td>
            </tr>
	</div>

	<!--<div style="float:right;"> -->
            <tr>
                <!--<td>Please enter City: </td>-->
                <td><input type="text" name="Origin_cityName" placeholder="Enter City"></td>
            </tr>
	
	</div>

            <tr>
                <!--<td>Please enter State</td>-->
		<td><input type="text" name="Origin_stateName" placeholder="Enter State"></td>
<!--
		<select>
	<option value="AL">Alabama</option>
	<option value="AK">Alaska</option>
	<option value="AZ">Arizona</option>
	<option value="AR">Arkansas</option>
	<option value="CA">California</option>
	<option value="CO">Colorado</option>
	<option value="CT">Connecticut</option>
	<option value="DE">Delaware</option>
	<option value="DC">District Of Columbia</option>
	<option value="FL">Florida</option>
	<option value="GA">Georgia</option>
	<option value="HI">Hawaii</option>
	<option value="ID">Idaho</option>
	<option value="IL">Illinois</option>
	<option value="IN">Indiana</option>
	<option value="IA">Iowa</option>
	<option value="KS">Kansas</option>
	<option value="KY">Kentucky</option>
	<option value="LA">Louisiana</option>
	<option value="ME">Maine</option>
	<option value="MD">Maryland</option>
	<option value="MA">Massachusetts</option>
	<option value="MI">Michigan</option>
	<option value="MN">Minnesota</option>
	<option value="MS">Mississippi</option>
	<option value="MO">Missouri</option>
	<option value="MT">Montana</option>
	<option value="NE">Nebraska</option>
	<option value="NV">Nevada</option>
	<option value="NH">New Hampshire</option>
	<option value="NJ">New Jersey</option>
	<option value="NM">New Mexico</option>
	<option value="NY">New York</option>
	<option value="NC">North Carolina</option>
	<option value="ND">North Dakota</option>
	<option value="OH">Ohio</option>
	<option value="OK">Oklahoma</option>
	<option value="OR">Oregon</option>
	<option value="PA">Pennsylvania</option>
	<option value="RI">Rhode Island</option>
	<option value="SC">South Carolina</option>
	<option value="SD">South Dakota</option>
	<option value="TN">Tennessee</option>
	<option value="TX">Texas</option>
	<option value="UT">Utah</option>
	<option value="VT">Vermont</option>
	<option value="VA">Virginia</option>
	<option value="WA">Washington</option>
	<option value="WV">West Virginia</option>
	<option value="WI">Wisconsin</option>
	<option value="WY">Wyoming</option>
</select>	

               
                    <textarea name="Question" rows="6" cols="60"></textarea>
                </td>
		-->
            </tr>
		



		<tr>
                <!--<td>Please enter Zipcode: </td>-->
                <td><input type="text" name="Origin_Zipcode" placeholder="Enter Zipcode"></td>
            </tr>
            <tr>
     <!--           <td><input type="submit" name="submit" value="post"></td>
            </tr>
	-->
</table></center>

<center><table>

<h3>Destination</h3>

    <form action = "menu_page.php" method="post">       
	<table>
	<div style="float:left;">
            <tr>
                <!--<td>Please enter Street: </td>-->
                <td><input type="text" name="Des_streetName" placeholder="Enter Street"></td>
            </tr>
	</div>

	<div style="float:right;">
            <tr>
                <!--<td>Please enter City: </td>-->
                <td><input type="text" name="Des_cityName" placeholder="Enter City"></td>
            </tr>
	
	</div>

            <tr>
                <!--<td>Please enter State</td>-->
		<td><input type="text" name="Des_stateName" placeholder="Enter State"></td>
                <!--<td>
                    <textarea name="Question" rows="6" cols="60"></textarea>
                </td>
		-->
            </tr>
		
		<tr>
                <!--<td>Please enter Zipcode: </td>-->
                <td><input type="text" name="Des_Zipcode" placeholder="Enter Zipcode"></td>
            </tr>

            <tr>
                <td><input type="submit" name="submit" value="post"></td>
            </tr>


        </table></center>
	<br>
	<br>
	 <input type="checkbox" id="save_destination_box" name="save_destination_box" value="true">   

    </form>

     <td>save destination</td>
    
<br>
<br>
<input type="button" onclick="location.href='main_menu.php';"value='main menu' />

</div>
</main>
</body>
</html>
