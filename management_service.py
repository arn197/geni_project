import socket
import sys
from threading import Thread
from queue import Queue
import time

RANGE_OF_CHARS = 52  # Include a-z and A-Z

# Generic function to receive a message from connected clients
# The data is received in chunks of 16 bytes with '\n' as the
# end of data marker


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

# Helper function to send a message back to client


def send_message(connection, msg):
    connection.sendall((msg + '\n').encode())

def measurement(start_time,end_time):	
    RTT = end_time-start_time	
    print(f'RTT: {RTT}')

class Client:
    def __init__(self, key, socket):
        self.key = key
        self.socket = socket

    def start(self, inputQueue, outputQueue):
        while True:
            req = inputQueue.get()
            try:
                send_message(self.socket, req)
                res = receive_message(self.socket)
                if res != "OK":
                    inputQueue.put(req)
                    break
                md5 = req.split("-")[0]
                msg = receive_message(self.socket)
                outputQueue.put(md5 + ":" + msg)
            except:
                break

class ClientManager:
    def __init__(self):
        self.clients = {}
        self.activeThreads = {}
        self.outputQueue = Queue()
        self.inputQueue = Queue()
        self.req_sent = False
        self.start_time = None	
        self.end_time = None

    def waitForResults(self):
        password = ""
        md5 = ""
        while True:
            data = self.outputQueue.get()
            md5 = data.split(":")[0]
            success = data.split(":")[1] == "SUCCESS"
            if success:
                password = data.split(":")[2]
                self.end_time = time.perf_counter()
                measurement(self.start_time,self.end_time)
                self.req_sent = False
                break
        return md5, password

    def add_client(self, key, connection):
        if receive_message(connection) == "READY":
            client = Client(key, connection)
            self.clients[key] = client
            workerThread = Thread(target=client.start, args=(self.inputQueue, self.outputQueue))
            workerThread.start()
        else:
            connection.close()
            return

    def new_request(self, md5, n_chars):
        n_clients = 1000
        totalRange = pow(RANGE_OF_CHARS, n_chars) - 1
        increment = int(totalRange/n_clients)
        overflow = totalRange % n_clients

        start = 0
        for i in range(n_clients):
            end = start + increment
            if i == n_clients - 1:
                end += overflow
            msg = str(md5) + "-" + str(start) + "-" + str(end) + "-" + str(n_chars)
            if self.req_sent == False:
                self.start_time = time.perf_counter()
                self.req_sent = True
            self.inputQueue.put(msg)
            start += increment

def listenForClients(sock, client_manager):
    # Listen for incoming connections
    while True:
        sock.listen(1)
        connection, client_address = sock.accept()
        key = str(client_address[0]) + "-" + str(client_address[1])
        client_manager.add_client(key, connection)


def start_server(port_number):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # if(len(sys.argv) < 2):
    #     print("Please enter a port number")
    #     exit()
    # port_number = int(sys.argv[1])

    server_address = (socket.gethostname(), port_number)
    sock.bind(server_address)

    client_manager = ClientManager()
    clientListener = Thread(target=listenForClients, args=(sock, client_manager))
    clientListener.start()
    return client_manager


if __name__ == "__main__":
    start_server(5000)
