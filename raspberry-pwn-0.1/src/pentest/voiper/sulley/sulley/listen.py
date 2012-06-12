from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('127.0.0.1', 5060))
while 1:
    data = s.recvfrom(256)
    print data
    
