"""
Name: Benton Speck, Dillon Hines, Adi Smith, Joel Carpenter
Date: March 22, 2019
Desc: TCP like implementation using UDP
"""
import pickle
import socket
import math 

segment_size = 500

def Decrypt(shift, text):
   
    stringList = []
    newLine = []
    ret = ""
    for x in text:
        stringList.append(x)
    print(stringList)
    for x in stringList:
        line =  list(x)
        for y in line:
            if(y.isalpha()): 
                newLine.append(chr(ord(y) - shift))
            else:
                newLine.append(y)
    print(newLine)
    for i in newLine:
        ret += i
    ##print(ret)

def Encrypt(shift, text):
   
    stringList = []
    newLine = []
    ret = ""
    for x in text:
        stringList.append(x)
    print(stringList)
    for x in stringList:
        line =  list(x)
        for y in line:
            if(y.isalpha()): 
                newLine.append(chr(ord(y) + shift))
            else:
                newLine.append(y)
    print(newLine)
    for i in newLine:
        ret += i
    ##print(ret)
    return ret
        

class BigUDP:
    def __init__(self):
        pass

    def sendto(self, message, destination, key, password):
        # Opens up a socket for message transfer
        msg = Encrypt(key, message)
        safety = Encrypt(key, password)
        
        sender = safety + msg
        s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        # Pickles the message to be split up and sent
        temp = pickle.dumps(sender)
        # If the pickled message size is larger than the segment size, split it up
        if len(temp) > segment_size:
            # Amount of 'packets' we will be sending
            total_packets = math.ceil(len(temp) / segment_size)
            # Splits up the packets
            for i in range(total_packets):
                # This creates a segmented message to be sent as a packet
                ret = temp[(segment_size * i) : (segment_size * (i + 1))]
                # Assign segment, packet number, and total packet number as a packet
                raw = (ret, i, total_packets)
                to_send = pickle.dumps(raw)
                s.sendto(to_send, destination)
        # Else, pickle and send
        else:
            ret = pickle.dumps((temp, 0, 1))
            s.sendto(ret, destination)

    def recvfrom(self, mybind, timeout = 5):
        # Opens up a socket for message transfer
        s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        # Binds the socket
        s.bind(mybind)
        # Receives the first packet that is sent
        (raw, addr) = s.recvfrom(1024)
        # Un-pickles the packet
        temp = pickle.loads(raw)
        # Creates a byte array to store the original pickled message after assembly
        ret = bytearray(temp[2] * segment_size)
        # Assigns the first packet to the appropriate spot in the byte array
        ret[(segment_size * temp[1]) : (segment_size * (temp[1] + 1))] = temp[0]
        # Sets timeout given via arguments
        s.settimeout(timeout)
        # Counter to break loop after all packets are received / assembled
        received = 1
        while True:
            # If s.recvfrom times out, an exception is thrown
            try:
                # Break out of the loop if received (packets received) is equal to temp[2] (total packets to receive)
                if received == temp[2]:
                    break
                # Receives pickled tuple (data, packet number, total packets)
                (raw, addr) = s.recvfrom(1024)
                # Unpickles the tuple
                temp = pickle.loads(raw)
                # Assigns the packet to the appropriate spot in the byte array
                ret[(segment_size * temp[1]) : (segment_size * (temp[1] + 1))] = temp[0]
                received += 1
            # If timeout occurs, return None to the address
            except:
                return (None, addr)
        # Since ret is a bytearray composed of the individual packets of the original pickled message, we need to
        # unpickle it to get the original message sent
        ret = pickle.loads(ret)
        if Decrypt(2, ret) == 0 :
            print("password is wrong")
            return
                
        return (ret, addr)
