<?php
$servername = "localhost";
$username = "root";
$password = "mypass";
$file = fopen("./soh.csv","r");
// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
//echo "Connected successfully";
mysqli_select_db($conn,"data");
while(!feof($file))
  {
    $sku = fgetcsv($file)[0];
    $name = fgetcsv($file)[1];
    $price = fgetcsv($file)[2];


    if(trim($code) != "" && trim($item) != "" && trim($price) != ""){
      $sql = "INSERT INTO appdata SET code='$code',item='$item',price='$price';";
      //echo $sql;
      if($conn->query($sql)){
        echo "successfully";
      }else{
        echo("Error description: " . mysqli_error($conn));
      }
    }

  }

fclose($file);
?>
