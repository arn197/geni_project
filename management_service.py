import socket
import sys
from threading import Thread
from queue import Queue

RANGE_OF_CHARS = 52  # Include a-z and A-Z

# Generic function to receive a message from connected clients
# The data is received in chunks of 16 bytes with '\n' as the
# end of data marker
def receive_message(connection):
    msg = ""
    while True:
        data = connection.recv(16).decode()
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

class Client:
    def __init__(self, id, client_address, socket):
        self.client_address = client_address
        self.socket = socket
        self.id = id
    
    def send_req(self, md5, start, end):
        msg = str(md5) + "-" + str(start) + "-" + str(end)
        send_message(self.socket, msg)
        res = receive_message(self.socket)
        if res == "OK":
            return True
        return False
    
    def waitForResults(self, outputQueue):
        msg = receive_message(self.socket)
        outputQueue.put(str(self.id) + ":" + msg)

class ClientManager:
    def __init__(self):
        self.clients = {}
        self.latestID = 0
        self.activeThreads = {}
        self.outputQueue = Queue()

    def waitForResults(self):
        while True:
            data = self.outputQueue.get()
            clientID = int(data.split(":")[0])
            self.activeThreads[clientID].join()
            print(data)

    def add_client(self, client_address, connection):
        newID = self.latestID
        send_message(connection, str(newID))
        if receive_message(connection) == "OK":
            self.latestID += 1
            client = Client(newID, client_address, connection)
            self.clients[newID] = client
        else:
            connection.close()
            return

    def get_free_clients(self):
        free_clients = []
        for i in range(self.latestID):
            if i not in self.activeThreads:
                free_clients.append(i)
        return free_clients

    def new_request(self, md5, n_chars):
        free_clients = self.get_free_clients()
        n_clients = len(free_clients)
        totalRange = pow(RANGE_OF_CHARS, n_chars)
        increment = int(totalRange/n_clients)
        overflow = totalRange%n_clients
        start = 0

        count = 0

        for i in range(n_clients):
            freeClient = self.clients[free_clients[i]]
            end = start + increment
            if i == n_clients - 1:
                end += overflow
            if freeClient.send_req(start, end):
                start += increment
                count += 1
                workerThread = Thread(target=freeClient.waitForResults, args=(self.outputQueue))
                workerThread.start()
                self.activeThreads[free_clients[i]] = workerThread
        
        if count > 0:
            print('Divided work among ' + str(count) + ' workers')
        else:
            print('Error dividing work. Please try again')

def start_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if(len(sys.argv) < 2):
        print("Please enter a port number")
        exit()
    port_number = int(sys.argv[1])

    server_address = (socket.gethostname(), port_number)
    sock.bind(server_address)

    client_manager = ClientManager()

    # Listen for incoming connections
    while True:
        sock.listen(1)
        connection, client_address = sock.accept()

        client_manager.add_client(client_address, connection)


if __name__ == "__main__":
    start_server()
