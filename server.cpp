/**
 * @file server.cpp
 * @author Enrique Cavanillas Puga
 * @brief This is a dummy-test echo server using TCP protocol.
 * @version 0.2
 * @date 2022-06-26
 * 
 */


#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>

#define BUF_SIZE 500
#define MAX_CONNECTION_REQUESTS 1

int main(int argc, char *argv[])
{

    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s server %s port\n", argv[0], argv[1]);
        exit(EXIT_FAILURE);
    }

    struct addrinfo hints;
    struct addrinfo *result, *rp;
    sockaddr_storage addr;
    socklen_t addrlen = sizeof(addr);
    int s, sfd, clsfd, rcv;
    char host[NI_MAXHOST], serv[NI_MAXSERV], buf[BUF_SIZE];


    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_UNSPEC;    /* Allow IPv4 or IPv6 */
    hints.ai_flags = 0;
    hints.ai_socktype = SOCK_STREAM; /* Datagram socket */
    hints.ai_protocol = 0;          /* Any protocol */
    hints.ai_canonname = NULL;
    hints.ai_addr = NULL;
    hints.ai_next = NULL;

    if (getaddrinfo(argv[1], argv[2], &hints, &result))
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
        exit(EXIT_FAILURE);
    }

    /* getaddrinfo() returns a list of address structures.
       Try each address until we successfully bind(2).
       If socket(2) (or bind(2)) fails, we (close the socket
       and) try the next address. */
    for (rp = result; rp != NULL; rp = rp->ai_next)
    {
        sfd = socket(rp->ai_family, rp->ai_socktype,
                     rp->ai_protocol);
        if (sfd == -1)
            continue;

        if (bind(sfd, rp->ai_addr, rp->ai_addrlen) == 0)
            break; /* Success */

        close(sfd);
    }

    if (rp == NULL)
    { /* No address succeeded */
        fprintf(stderr, "Could not bind\n");
        exit(EXIT_FAILURE);
    }

    freeaddrinfo(result); /* No longer needed */

    if (listen(sfd, MAX_CONNECTION_REQUESTS))
    {
        fprintf(stderr,"Error listening\n");
        exit(EXIT_FAILURE);
    }

    /* Read datagrams and echo them back to sender */

    while (true)
    {
        clsfd = accept(sfd, (sockaddr*)&addr, &addrlen);
        getnameinfo((sockaddr *)&addr,
                        addrlen, host, NI_MAXHOST,
                        serv, NI_MAXSERV, NI_NUMERICHOST | NI_NUMERICSERV);
        printf("Connection from %s:%s\n", host, serv);

        while(rcv = recv(clsfd, buf, BUF_SIZE, 0))
        {
            buf[rcv] = '\0';
            printf("\tRecieved: %s", buf);
            send(clsfd, buf, rcv, 0);
            sleep(1);
        }

        close(clsfd);
        printf("Connection closed: %s:%s\n", host, serv);
    }
    
    return 0;
}