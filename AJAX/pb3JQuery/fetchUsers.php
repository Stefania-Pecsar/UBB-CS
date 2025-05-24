<?php
$con = mysqli_connect("localhost", "root", "", "tren");
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

// Fetch all users
$result = mysqli_query($con, "SELECT * FROM users");

$users = array();
while($row = mysqli_fetch_assoc($result)) {
    $users[] = $row;
}

mysqli_close($con);

echo json_encode($users);
?>