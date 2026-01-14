<?php
$con = mysqli_connect("localhost", "root", "", "tren");
if (!$con) {
    die('Could not connect: ' . mysqli_error());
}

$result = mysqli_query($con, "SELECT orasSosire FROM tren WHERE orasPlecare = '" .$_GET["name"] ."'");

while ($row = mysqli_fetch_array($result)) {
    echo "<option value='" . $row[0] . "'>" . $row[0] . "</option>";
}
mysqli_close($con);
?>