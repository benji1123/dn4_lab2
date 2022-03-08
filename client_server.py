#!/usr/bin/python3

from shutil import register_archive_format
import socket
import argparse
import sys
import getpass
import hashlib
from quopri import decodestring
from csv_handler import * 

HOSTNAME = "0.0.0.0"      # All interfaces.
PORT = 8000
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
GET_GRADES_CMD = "GG"

COL_NAMES = {
    "L1" : "Lab 1", 
    "L2" : "Lab 2", 
    "L3" : "Lab 3", 
    "L4" : "Lab 4", 
    "M" : "Midterm", 
    "E1" : "Exam 1", 
    "E2" : "Exam 2", 
    "E3" : "Exam 3", 
    "E4" : "Exam 4"
}


########################################################################
# Echo Server class
########################################################################


class Server:
    RECV_BUFFER_SIZE = 1024 # Used for recv.
    MAX_CONNECTION_BACKLOG = 10
    MSG_ENCODING = "utf-8" # Unicode text encoding.
    csv_handler = csv_handler()
    
    def __init__(self):
        self.create_listen_socket()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(SOCKET_ADDRESS)
            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            print("Listening on port {} ...".format(PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            self.socket.close()
            sys.exit(1)

    def handle_get_grade(self, recvd_str):
        ID_INDEX = 0
        PW_INDEX = 1
        recvd_hash = recvd_str.split(" ")[1]
        print(f"Received ID/password hash <{recvd_hash}> from client.")
        l = self.csv_handler.get_ids_and_passwords()
        for i in l:
            h = str(create_hash(i[ID_INDEX], i[PW_INDEX]))
            if h == recvd_hash:
                print("Correct password, record found")
                send_str = self.csv_handler.get_all_grades(i[ID_INDEX])
                return send_str
        print("Password failure")
        return

    def connection_handler(self, client):
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))
        # Output the socket address.
        print(client)

        while True:
            try:
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)
                if len(recvd_bytes) == 0:
                    print("Closing client connection ... ")
                    connection.close()
                    break
                
                recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
                print("Command received: ", recvd_str)

                if recvd_str == GET_MIDTERM_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("M")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_LAB_1_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("L1")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_LAB_2_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("L2")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
                
                elif recvd_str == GET_LAB_3_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("L3")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_LAB_4_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("L4")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_EXAM_1_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("E1")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_EXAM_2_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("E2")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_EXAM_3_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("E3")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif recvd_str == GET_EXAM_4_AVG_CMD:
                    send_str = self.csv_handler.get_category_mean("E4")
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))

                elif len(recvd_str) > 1 and recvd_str[0:2] == GET_GRADES_CMD:
                    send_str = self.handle_get_grade(recvd_str)
                    connection.sendall(str(send_str).encode(Server.MSG_ENCODING))
            except KeyboardInterrupt:
                print()
                print("Closing client connection ... ")
                connection.close()
                break


########################################################################
# Echo Client class
########################################################################


class Client:
    RECV_BUFFER_SIZE = 128 # Used for recv.    
    def __init__(self):
        self.get_socket()
        self.connect_to_server()
        self.send_console_input_forever()

    def get_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            self.socket.connect((HOSTNAME, PORT))
            print("Connected to \"{}\" on port {}".format(HOSTNAME, PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        while True:
            self.input_text = input("Input: ")
            if self.input_text != "":
                print(f"Command entered: {self.input_text}")
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
                self.socket.close()
                sys.exit(1)
                
    def connection_sendall(self):
        try:
            if self.input_text == GET_GRADES_CMD:
                id = getpass.getpass(prompt = "Enter student ID number: ")
                pw = getpass.getpass(prompt = "Enter password: ")
                print(f"ID number <{id}> and password <{pw}> received")
                h = str(create_hash(id, pw))
                print(f"ID/password hash <{h}> sent to server.")
                self.input_text += " " + h
            if self.input_text[0] == 'G' and self.input_text[-1] == 'A':
                print(f"Fetching {self.input_text[1:-1]} grades")
            self.socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)
            print(f"Received: {recvd_bytes.decode(Server.MSG_ENCODING)}\n")
        except Exception as msg:
            print(msg)
            sys.exit(1)


def create_hash(id, pw):
    id = id.encode(encoding = 'UTF-8') #encode id using UTF-8
    pw = pw.encode(encoding = 'UTF-8') #encode password using UTF-8
    hash = hashlib.sha256() #initialize SHA-256 hash object
    hash.update(id) #update hash object with the bytes-like object
    hash.update(pw) #repeated calls are equivalent to single call with concatenation of all arguments
    return hash.digest() #return the digest of the data passed to the update()


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