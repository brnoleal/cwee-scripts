import hashlib
import sys

def pw_hash(password):
    salt = 'it6z'
    hash_object = hashlib.md5((salt + password).encode())
    return hash_object.hexdigest()

def main():
    try:
        number = 0
        while True:
            password = str(number)
            hashed_value = pw_hash(password)
            # Check if hash starts with '0e' and has numbers after 'e'
            if hashed_value.startswith('0e') and hashed_value[2:].isdigit():
                print(f"Found hash starting with '0e', followed by numbers:")
                print(f"Password: {password}")
                print(f"Hash: {hashed_value}")
                break
            number += 1
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
