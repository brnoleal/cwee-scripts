import sqlite3
import hashlib
import base64


# Variables for email and password
email = "bmdyy@pass2.htb"
password = "$2a$12$cL8f8M6VTPILtTStdqmLrunDy4JW/FbNYVpfJnLO2XoZGs/c7E2IG"

def calculate_secret_key():
    try:
        # Combine email and password with the salt
        tmp = email + "$4lty" + password

        # Compute the SHA-256 hash
        digest = hashlib.sha256(tmp.encode('utf-8')).digest()

        # Encode the hash in Base64 and replace '-' and '_' with 'X'
        b64 = base64.urlsafe_b64encode(digest).decode('utf-8').replace('-', 'X').replace('_', 'X')

        # Format the secret key
        secret_key = f"{b64[:4]}-{b64[4:8]}-{b64[8:12]}-{b64[12:16]}"

        return secret_key
    except Exception as e:
        print(f"Error: {e}")
        return None


# Example usage
secret_key = calculate_secret_key()
if secret_key:
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Secret Key: {secret_key}")
else:
    print("User not found or error occurred.")
