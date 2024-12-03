<?php
$salt = "it6z";
// $password = [];
$hashed_value = md5($salt . $password);
echo $hashed_value;
?>
