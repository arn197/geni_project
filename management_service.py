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

    def send_req(self, md5, start, end, n_chars):
        try:
            msg = str(md5) + "-" + str(start) + "-" + str(end) + "-" + str(n_chars)
            send_message(self.socket, msg)
            res = receive_message(self.socket)
            if res == "OK":
                return True
        except:
            pass
        return False
        

    def waitForResults(self, outputQueue):
        msg = receive_message(self.socket)
        outputQueue.put(str(self.key) + ":" + msg)

class ClientManager:
    def __init__(self):
        self.clients = {}
        self.activeThreads = {}
        self.outputQueue = Queue()
        self.req_sent = False
        self.start_time = None
        self.end_time = None

    def waitForResults(self):
        password = ""
        while True:
            if len(self.activeThreads) == 0:
                break
            data = self.outputQueue.get()
            clientID = data.split(":")[0]
            success = data.split(":")[1] == "SUCCESS"
            self.activeThreads[clientID].join()
            self.activeThreads.pop(clientID)
            if success:
                password = data.split(":")[2]
                self.end_time = time.perf_counter()   
                measurement(self.start_time,self.end_time)
                self.req_sent = False   
        return password

    def add_client(self, key, connection):
        if receive_message(connection) == "READY":
            client = Client(key, connection)
            self.clients[key] = client
        else:
            connection.close()
            return

    def get_free_clients(self):
        free_clients = []
        to_pop = []
        for key in self.clients:
            client = self.clients[key]
            if key not in self.activeThreads:
                try:
                    send_message(client.socket, "READY?")
                    if receive_message(client.socket) == "READY":
                        free_clients.append(client)
                except:
                    to_pop.append(client)
        for i in to_pop:
            self.clients.pop(i.key)
        return free_clients

    def new_request(self, md5, n_chars):
        free_clients = self.get_free_clients()
        n_clients = len(free_clients)
        totalRange = pow(RANGE_OF_CHARS, n_chars) - 1
        increment = int(totalRange/n_clients)
        overflow = totalRange % n_clients

        start = 0   
        count = 0
        for i in range(n_clients):
            freeClient = free_clients[i]
            end = start + increment
            if i == n_clients - 1:
                end += overflow
            if freeClient.send_req(md5, start, end, n_chars):
                if self.req_sent == False:
                    self.start_time = time.perf_counter()
                    self.req_sent = True
                start += increment
                count += 1
                workerThread = Thread(
                    target=freeClient.waitForResults, args=(self.outputQueue,))
                workerThread.start()
                self.activeThreads[free_clients[i].key] = workerThread

        if count > 0:
            print('Divided work among ' + str(count) + ' workers')
        else:
            print('Error dividing work. Please try again')


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
    #print(server_address[0])

    client_manager = ClientManager()
    clientListener = Thread(target=listenForClients, args=(sock, client_manager))
    clientListener.start()
    return client_manager


if __name__ == "__main__":
    start_server(5000)
