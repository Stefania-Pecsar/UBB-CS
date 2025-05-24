<?php
$con = mysqli_connect("localhost", "root", "", "tren");
if (!$con) {
    die('Could not connect: ' . mysqli_error());
}

$orasPlecare = mysqli_real_escape_string($con, $_GET["name"]);

$result = mysqli_query($con, "SELECT orasSosire FROM tren WHERE orasPlecare = '$orasPlecare'");

while ($row = mysqli_fetch_array($result)) {
    echo "<option value='" . htmlspecialchars($row[0]) . "'>" . htmlspecialchars($row[0]) . "</option>";
}
mysqli_close($con);
?>