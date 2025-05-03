<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once(__DIR__ . '/wp-config.php');

$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
if ($mysqli->connect_error) {
    die("Database connection failed: " . $mysqli->connect_error);
}

$sql = "SELECT ID, user_login, user_email, user_nicename, display_name, user_pass FROM wp_users";
$result = $mysqli->query($sql);

if (!$result) {
    die("Query error: " . $mysqli->error);
}

echo "WordPress users:\n\n";

while ($row = $result->fetch_assoc()) {
    echo "ID:           " . $row['ID'] . "\n";
    echo "Login:        " . $row['user_login'] . "\n";
    echo "Email:        " . $row['user_email'] . "\n";
    echo "Nicename:     " . $row['user_nicename'] . "\n";
    echo "Display Name: " . $row['display_name'] . "\n";
    echo "Password Hash:" . $row['user_pass'] . "\n";
    echo "-----------------------------\n";
}

$mysqli->close();
?>
