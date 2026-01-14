<?php
$con = mysqli_connect("localhost", "root", "", "tren");
if (!$con) {
    die('Could not connect: ' . mysqli_error());
}

$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$items_per_page = 3;
$offset = ($page - 1) * $items_per_page;

$stmt = $con->prepare("SELECT nume, prenume, telefon, email FROM users LIMIT ?, ?");
$stmt->bind_param("ii", $offset, $items_per_page);
$stmt->execute();
$result = $stmt->get_result();
$data = array();
while($row = mysqli_fetch_assoc($result)) {
    $data[] = $row;
}

$count_result = mysqli_query($con, "SELECT COUNT(*) as total FROM users");
$count_row = mysqli_fetch_assoc($count_result);
$total_count = $count_row['total'];

echo json_encode(array('data' => $data, 'total' => $total_count));

mysqli_close($con);
?>