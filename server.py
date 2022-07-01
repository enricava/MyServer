"""
Echo server
v 0.1
"""
import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 2222)
print('[+] Server starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('[+] Waiting for connections')
    connection, client_address = sock.accept()
    try:
        print('[+] Connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('[+] Received {!r}'.format(data))
            if data:
                print('[+] Sending data back to the client')
                connection.sendall(data)
            else:
                print('[+] Received no data', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()