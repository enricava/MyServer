"""
Echo client
v 0.1
"""
import socket
import sys

from protocol import Message

PACKET_SIZE = 255

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 2223)
print('[+] Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send data
    message = b'This is the message.  It will be repeated.'
    print('[+] Sending {!r}'.format(message))
    m = Message('b','client','server', message)
    packets = m.pack(PACKET_SIZE)
    for packet in packets:
        sock.sendall(packet)

    contents = b''
    eom = 0
    while eom != 1:
        received = sock.recv(PACKET_SIZE)
        code, type, origin, dest, data, eom = Message.unpack(received)
        contents += data
        
        
    print(contents)


finally:
    print('[+] Closing socket')
    sock.close()