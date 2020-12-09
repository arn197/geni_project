import socket
import sys
from threading import Thread
from collections import deque
import hashlib


"""
Helper function to convert an integer to base 52 and return as a string.

input: (int) A number in the possible range.
output: (str) Base 52 equivalent of the number.

"""
def numtobase(data):
    str = "ABCDEFGHIJKLNMOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #str = "123456789ABCDEF"
    s = ""
    if data == 0:
        return str[0] + ""

    while data>0:
        if data<52:
            s = str[data] + s
            data = 0
            #print(s)
        else:
            r = data%52
            s = str[r] + s
            data = (data-r)//52
            #print(s)
    return s

"""
Helper function to receive messages.
input: Socket
"""
def receive_message(connection):
    msg = ""
    while True:
        data = connection.recv(1).decode()
        if data:
            msg += data
        else:
            break
        if '\n' in msg:
            break
    return msg.rstrip()


"""
Helper function to send messages.
input: Socket, (str) message
"""
def send_message(connection,msg):
    connection.sendall((msg + '\n').encode())

"""
Helper function to convert a string to its md5 hash.

input: (str) Base 52 value of an integer in the range.
output : (str) md5 Hash.
"""
def generated_hash(data):               
    result = hashlib.md5(data.encode())
    return result.hexdigest()



"""
Helper function to compare md5 hash.

Input: (str) input md5 hash, (str) calculated md5 hash.
Output: boolean
"""
def compareHash(actual, determined):
    if determined == actual:
        return True


class Worker:
    def __init__(self):
        self.sock = None

    def startWorkers(self,address, port_num):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address , port_num)
        self.sock.connect(server_address)
        #msg = str(self.client_id) + " Connected to server"
        #send_message(self.sock,msg)
        #msg = receive_message(self.sock)
        send_message(self.sock, "READY")
        while True:
            self.getrequest(self.sock)

    def getrequest(self,socket):
        msg = receive_message(socket)
        temp = msg.split('-')
        md5 = temp[0]
        start = int(temp[1])
        end = int(temp[2])
        num_char = int(temp[3])
        send_message(socket, "OK")
        self.startCracking(md5,start,end,num_char)

    def end_connection(self,socket):
        socket.close()


    def startCracking(self, md5,start,end,num_char):
        res, pwd = self.crack(md5,start,end,num_char)
        if res == True:
            print("SUCCESS")
            send_message(self.sock,"SUCCESS:" + pwd)
        else:
            print("FAIL")
            send_message(self.sock,"FAIL:")
        return
    
                    
    def crack(self,md5,start,end,num_char):
        st = start
        en = end
        for i in range(st,en+1):
            value = numtobase(i)
            offset = num_char-len(value)
            temp = 'A'*offset + value
            determined = generated_hash(temp)
            if compareHash(md5,determined):
                return True , temp
        return False, ""


def main():
    address = sys.argv[1]
    port_number = int(sys.argv[2])
    work = Worker()
    work.startWorkers(address,port_number)

if __name__ == "__main__":
    main()

#Shoumik-ElementryOS