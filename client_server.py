#!/usr/bin/python3

"""
Echo Client and Server Classes

T. D. Todd
McMaster University

to create a Client: "python EchoClientServer.py -r client" 
to create a Server: "python EchoClientServer.py -r server" 

or you can import the module into another file, e.g., 
import EchoClientServer
e.g., then do EchoClientserver.Server()

"""

########################################################################

import socket
import argparse
import sys
import getpass
import hashlib
from quopri import decodestring
from csv_handler import * 

HOSTNAME = "0.0.0.0"      # All interfaces.
PORT = 5000
SOCKET_ADDRESS = (HOSTNAME, PORT)

GET_LAB_1_AVG_CMD = "GL1A"
GET_LAB_2_AVG_CMD = "GL2A"
GET_LAB_3_AVG_CMD = "GL3A"
GET_LAB_4_AVG_CMD = "GL4A"
GET_MIDTERM_AVG_CMD = "GMA"
GET_EXAM_1_AVG_CMD = "GE1A"
GET_EXAM_2_AVG_CMD = "GE2A"
GET_EXAM_3_AVG_CMD = "GE3A"
GET_EXAM_4_AVG_CMD = "GE4A"

########################################################################
# Echo Server class
########################################################################

class Server:

    # Set the server hostname used to define the server socket address
    # binding. Note that "0.0.0.0" or "" serves as INADDR_ANY. i.e.,
    # bind to all local network interfaces.
    # HOSTNAME = "192.168.1.22" # single interface
    # HOSTNAME = "hornet"       # valid hostname (mapped to address/IF)
    # HOSTNAME = "localhost"    # local host (mapped to local address/IF)
    # HOSTNAME = "127.0.0.1"    # same as localhost
    
    RECV_BUFFER_SIZE = 1024 # Used for recv.
    MAX_CONNECTION_BACKLOG = 10

    # We are sending text strings and the encoding to bytes must be
    # specified.
    # MSG_ENCODING = "ascii" # ASCII text encoding.
    MSG_ENCODING = "utf-8" # Unicode text encoding.

    # Create server socket address. It is a tuple containing
    # address/hostname and port.
    
    def __init__(self):
        self.create_listen_socket()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set socket layer socket options. This one allows us to
            # reuse the socket without waiting for any timeouts.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind(SOCKET_ADDRESS)

            # Set socket to listen state.
            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            print("Listening on port {} ...".format(PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                # Block while waiting for accepting incoming TCP
                # connections. When one is accepted, pass the new
                # (cloned) socket info to the connection handler
                # function. Accept returns a tuple consisting of a
                # connection reference and the remote socket address.
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            # If something bad happens, make sure that we close the
            # socket.
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        # Unpack the client socket address tuple.
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))
        # Output the socket address.
        print(client)

        c = csv_handler()

        while True:
            try:
                # Receive bytes over the TCP connection. This will block
                # until "at least 1 byte or more" is available.
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)
            
                # If recv returns with zero bytes, the other end of the
                # TCP connection has closed (The other end is probably in
                # FIN WAIT 2 and we are in CLOSE WAIT.). If so, close the
                # server end of the connection and get the next client
                # connection.
                if len(recvd_bytes) == 0:
                    print("Closing client connection ... ")
                    connection.close()
                    break
                
                # Decode the received bytes back into strings. Then output
                # them.
                recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
                print("Received: ", recvd_str)

                if recvd_str == GET_MIDTERM_AVG_CMD:
                    send_str = c.get_category_mean("M")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_LAB_1_AVG_CMD:
                    send_str = c.get_category_mean("L1")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_LAB_2_AVG_CMD:
                    send_str = c.get_category_mean("L2")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break
                
                elif recvd_str == GET_LAB_3_AVG_CMD:
                    send_str = c.get_category_mean("L3")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_LAB_4_AVG_CMD:
                    send_str = c.get_category_mean("L4")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_EXAM_1_AVG_CMD:
                    send_str = c.get_category_mean("E1")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_EXAM_2_AVG_CMD:
                    send_str = c.get_category_mean("E2")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_EXAM_3_AVG_CMD:
                    send_str = c.get_category_mean("E3")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_EXAM_4_AVG_CMD:
                    send_str = c.get_category_mean("E4")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                    break

                elif recvd_str == GET_GRADES_CMD:
                    # need student num
                    # send_str = c.get_all_grades()
                    break

                else:
                    #PASSWORD STUFF
                    break

            except KeyboardInterrupt:
                print()
                print("Closing client connection ... ")
                connection.close()
                break

########################################################################
# Echo Client class
########################################################################

class Client:

    # Set the server to connect to. If the server and client are running
    # on the same machine, we can use the current hostname.
    # SERVER_HOSTNAME = socket.gethostname()
    # SERVER_HOSTNAME = "localhost"
    
    # Try connecting to the compeng4dn4 echo server. You need to change
    # the destination port to 50007 in the connect function below.
    # SERVER_HOSTNAME = 'compeng4dn4.mooo.com'

    RECV_BUFFER_SIZE = 5 # Used for recv.    
    # RECV_BUFFER_SIZE = 1024 # Used for recv.

    def __init__(self):
        self.get_socket()
        self.connect_to_server()
        self.send_console_input_forever()

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow us to bind to the same port right away.            
            # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the client socket to a particular address/port.
            # self.socket.bind((Client.HOSTNAME, 40000))
                
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((HOSTNAME, PORT))
            print("Connected to \"{}\" on port {}".format(HOSTNAME, PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered, i.e., ignore blank lines.
        while True:
            self.input_text = input("Input: ")
            if self.input_text != "":
                break
    
    def send_console_input_forever(self):
        while True:
            try:
                self.get_console_input()
                self.connection_sendall()
                self.connection_receive()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Closing server connection ...")
                # If we get and error or keyboard interrupt, make sure
                # that we close the socket.
                self.socket.close()
                sys.exit(1)
                
    def connection_sendall(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)

            print("Received: ", recvd_bytes.decode(Server.MSG_ENCODING))

        except Exception as msg:
            print(msg)
            sys.exit(1)

########################################################################
# Authentication
########################################################################

def create_hash(id, pw):
    id = id.encode(encoding = 'UTF-8') #encode id using UTF-8
    pw = pw.encode(encoding = 'UTF-8') #encode password using UTF-8
    hash = hashlib.sha256() #initialize SHA-256 hash object
    hash.update(id) #update hash object with the bytes-like object
    hash.update(pw) #repeated calls are equivalent to single call with concatenation of all arguments
    return hash.digest() #return the digest of the data passed to the update()

########################################################################
# Process command line arguments if this module is run directly.
########################################################################

# When the python interpreter runs this module directly (rather than
# importing it into another file) it sets the __name__ variable to a
# value of "__main__". If this file is imported from another module,
# then __name__ will be set to that module's name.

if __name__ == '__main__':
    roles = {'client': Client,'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles, 
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()

########################################################################
