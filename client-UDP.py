import socket

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = '10.18.101.97'
print("I am {}".format(host))

while True:
    password = input("Whats the password\n")
    
    message = input("what do you want to send\n")
    
    s.sendto(message.encode('ascii'), (host, port), 2, password )
