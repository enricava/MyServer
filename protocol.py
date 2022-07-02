from email import message
from random import randint
import re

class Message():

    def __init__(self, type: str, origin: str, dest: str, data: bytes) -> None:
        self.type = type
        self.origin = origin
        self.dest = dest
        self.data = data

    def __str__(self) -> str:
        return '[Type:{},Orig:{},Dest:{}] {}'.format(self.type, self.origin, self.dest, self.data)

    def pack(self, maxsize: int): 
        """
        Divides data into a list of encapsulated packets

        returns: list of packets : list[bytes]
        """
        code = randint(0, 255)                   # prevent mixtures among messages
        header = '{}:{}:{}:{}:'.format(code, self.type, self.origin, self.dest).encode()
        neom = b':1'     # not end of message
        eom = b':0'      # end of message
        protocol_length = len(header) + len(eom)
        packets = []
        packet_size = maxsize - protocol_length
        if packet_size <= 0:    # impossible to send
            return packets

        remaining = self.data
        while len(remaining) > packet_size:
            packets.append(header + remaining[:packet_size] + neom)
            remaining = remaining[packet_size:]
        packets.append(header + remaining + eom)
        return packets

    def unpack(self, packet):
        """
        TODO
        Receives single packet and returns contents

        returns: code, type, origin, dest, data, eom: bool
        """
        
        delimiters = [packet.find(b':')]
        for i in range(3):
            delimiters.append(packet.find(b':', delimiters[i]))
        [code, self.type, self.origin, self.dest] = [packet[i:delimiters[i]] for i in range(4)]
        data_end = packet.find(b':', )
        data = packet[delimiters[3] + 1 : -packet.reverse().find(b':',)]


#data = b'This is a test message. As you can see it will be sent in blocks'
#m = Message('b', 'henry', 'enrique', data)
#for elem in m.pack(30):
#    print(elem.decode())