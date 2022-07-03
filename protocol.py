from email import message
from random import randint
import re
from struct import pack

class Message():

    def __init__(self, type: str, origin: str, dest: str, data: bytes) -> None:
        assert ':' not in type+dest+origin 
        self.type = type
        self.origin = origin
        self.dest = dest
        self.data = data

    def __str__(self) -> str:
        return '[Type:{},Orig:{},Dest:{}] {}'.format(self.type, self.origin, self.dest, self.data)

    def pack(self, maxsize: int): 
        """
        Divides data into a list of encapsulated packets
        random_code:type:origin:dest:--data--:eom

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

    def unpack(packet):
        """
        TODO
        Receives single packet and returns contents

        returns: random code, type, origin, dest, data, eom: bool
        """
        
        delimiters = [0]
        for i in range(4):
            delimiters.append(packet.find(b':', delimiters[i]+1))

        [code, type, origin, dest] = [packet[delimiters[i]+min(i,1):delimiters[i+1]].decode() for i in range(4)]
        
        data = packet[delimiters[4]+1:packet.rfind(b':')]   
        eom = packet[-1:].decode()  
        
        return code, type, origin, dest, data, eom


#data = b'This is a test message. As you can see it will be sent in blocks'
#m = Message('b', 'henry', 'enrique', data)
#for elem in m.pack(26):
#    print(Message.unpack(elem))
#    if elem[5] == 0:
#        print('Message ended')