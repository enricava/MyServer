/**
 * @file client.cpp
 * @author Enrique Cavanillas Puga
 * @brief This is a dummy-test client that allows user to send text using TCP protocol.
 * @version 0.3
 * @date 2022-06-27
 * 
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define BUF_SIZE 64

/* For now the file name is a constant */
const char *filename = "dummy-client.txt";

bool receive_file(const char *filename, int sfd){
    FILE * fd = fopen(filename, "w");
    if (fd == NULL)
        return false;

    int c;
    char data[BUF_SIZE];
    while ((c = recv(sfd, data, BUF_SIZE, 0)) > 0){
        if (c < BUF_SIZE && data[c-1] == EOF)
            break;
        fwrite(data, c, 1, fd);
    }
    fclose(fd);
    printf("Received file\n");

    return true;
}

int main(int argc, char *argv[]){
    if (argc < 3){
        fprintf(stderr, "Usage: %s serv %s port msg...\n", argv[0], argv[1]);
        exit(EXIT_FAILURE);
    }

    struct addrinfo hints, *result, *rp;
    sockaddr_storage addr;
    socklen_t addrlen = sizeof(addr);
    int sfd;
    char buf[BUF_SIZE];

    /* Obtain address(es) matching host/port */

    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_UNSPEC;    /* Allow IPv4 or IPv6 */
    hints.ai_socktype = SOCK_STREAM; /* Datagram socket */
    hints.ai_flags = 0;
    hints.ai_protocol = 0; /* Any protocol */
    hints.ai_canonname = NULL;
    hints.ai_addr = NULL;
    hints.ai_next = NULL;

    if (getaddrinfo(argv[1], argv[2], &hints, &result)){
        fprintf(stderr, "Error: getaddrinfo %s : %s\n", argv[1], argv[2]);
        exit(EXIT_FAILURE);
    }

    /*getaddrinfo() returns a list of address structures.
    Try each address until we successfully connect(2).
    If socket(2)(or connect(2)) fails, we(close the socket and) try the next address.*/

    for (rp = result; rp != NULL; rp = rp->ai_next) {
        sfd = socket(rp->ai_family, rp->ai_socktype,
                     rp->ai_protocol);
        if (sfd == -1)
            continue;

        if (connect(sfd, rp->ai_addr, rp->ai_addrlen) != -1)
            break; /* Success */

        close(sfd);
    }

    if (rp == NULL){ /* No address succeeded */
        fprintf(stderr, "Could not connect\n");
        exit(EXIT_FAILURE);
    }

    freeaddrinfo(result); /* No longer needed */

    while (true) {
        int c = read(0, buf, BUF_SIZE);     /* Read client input */
        buf[c] = '\0';
        if (buf[0] == 'q' && c == 2){
            close(sfd);
            printf("Closing connection\n");
            exit(EXIT_SUCCESS);
        }
        send(sfd, buf, c, 0);               /* Send client input */
        c = recv(sfd, buf, BUF_SIZE, 0);    /* Read server message */
        buf[c] = '\0';
        printf("\tServer: %s",buf);
        printf("Receiving file\n");
        receive_file(filename, sfd);        /* Receives and saves file sent by server */

    }

    exit(EXIT_SUCCESS);
}
