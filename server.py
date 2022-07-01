"""
Echo server
v 0.2
"""
from http import client
import socket
import os

def server_init(num_connections=5):
    """
    Creates TCP socket, binds and listens.
    Starts dispatcher.

    param1: number of simultaneous connectons (int)
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 2222)
    print('[+] Server starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(num_connections)

    active_children = []

    run_dispatcher(sock, active_children)



def handle_connection(connection, client_address):
    """
    Handles new connection.
    """
    pid = os.getpid()
    try:
        print( pid, '[+] Connection from',client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print( pid, '[+] Received {!r}'.format(data))
            if data:
                print( pid, '[+] Sending data back to the client')
                connection.sendall(data)
            else:
                print( pid, '[+] Received no data', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
        os._exit(0)


def run_dispatcher(sock, active_children):
    """
    Handles multi-process connections

    param 1: tcp socket (socket)
    param 2: list of active children pids (list[int])
    """
    while True:
        # Wait for a connection, accept and fork
        print('[+] Waiting for connections')
        connection, client_address = sock.accept()
        child_pid = os.fork()
        if child_pid == 0:
            # Child process
            handle_connection(connection, client_address)
        else :
            # Parent process
            active_children.append(child_pid)

def main():
    server_init()

if __name__ == '__main__':
    main()