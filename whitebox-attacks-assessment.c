#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>

// Function to calculate MD5 hash
void pw_hash(const char *password, char *output) {
    char salt[] = "it6z";
    char input[256];
    unsigned char hash[MD5_DIGEST_LENGTH];

    strcpy(input, salt);
    strcat(input, password);
    
    MD5((unsigned char *)input, strlen(input), hash);

    for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
        sprintf(output + (i * 2), "%02x", hash[i]);
    }
    output[MD5_DIGEST_LENGTH * 2] = '\0';
}

int main() {
    int number = 0;
    char password[256];
    char hashed_value[MD5_DIGEST_LENGTH * 2 + 1];

    while (1) {
        sprintf(password, "%d", number);
        pw_hash(password, hashed_value);
        
        // Check if hash starts with '0e' and has digits after 'e'
        if (strncmp(hashed_value, "0e", 2) == 0) {
            int is_digit = 1;
            for (int i = 2; i < MD5_DIGEST_LENGTH * 2; i++) {
                if (!isdigit(hashed_value[i])) {
                    is_digit = 0;
                    break;
                }
            }
            if (is_digit) {
                printf("Found hash starting with '0e', followed by numbers:\n");
                printf("Password: %s\n", password);
                printf("Hash: %s\n", hashed_value);
                break;
            }
        }
        number++;
    }

    return 0;
}
