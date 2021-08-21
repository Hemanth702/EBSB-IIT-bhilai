<?php
         $dbhost = 'localhost';
         $dbuser = 'root';
         $dbpass = 'newPass@123';
		 $db = 'mail';
		 
         $conn = mysqli_connect($dbhost, $dbuser, $dbpass, $db);
         
         if(!$conn->connect_error ) {
            die('Could not connect: ' . $conn->connect_error);
         }
         echo 'Connected successfully';
         mysqli_close($conn);
      ?>