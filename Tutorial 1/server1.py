"""
server1.py

This file contains code for server1.py for Computer Networks (CS321),
Tutorial 1, server 1

The reason for each line of code is well commented, and it is taken care
that system is as robust as possible.

This work is tested on Python 3.8.5 [GCC 9.3.0] on Ubuntu 20.04.1 LTS
x86_64 Linux 5.4.0-5

work by Nivedit Jain (B18CSE039), jain.22@iitj.ac.in
"""

import sys  # to work with command line arguments
import socket  # for socket programming

# their must be at least one port given as command line argument
if len(sys.argv) < 2:
    raise Exception(f'{__file__} <port-number> ? (port not given in input)')

# server will accept only one argument <port>
if len(sys.argv) > 2:
    raise Exception(f'{__file__} <port-number> only accepts one argument <port-number')

# checking for the validity of port number
try:
    PORT = int(sys.argv[1])

    # port number cannot be negative
    if PORT < 0:
        raise ValueError("PORT number cannot be negative")

    # python sockets only allow positive 16 bit integers, so
    # port cannot be greater than 65535
    if PORT > 65535:
        raise ValueError("PORT number must be less than or equal to 65535")

except ValueError:
    raise Exception(f'<port-number> must be a valid unsigned 16-bit integer but given {sys.argv[1]}')

"""
If you want to set HOST Manually please change it to custom address string,
for example for local host, set

HOST = '127.0.0.1' 
in place of 
HOST = socket.gethostbyname(socket.gethostname())
"""

# getting host (IPv4) for sever system
HOST = socket.gethostbyname(socket.gethostname())

# MAX_TRANSFER_SIZE is 256 Bytes
MAX_TRANSFER_SIZE = 256

"""
handler functions below it 
"""


# calculate from query string
def calculate(message):
    # generating the list using spaces as separator
    data = message.split(' ')

    # checking if input has nothing more than an expression
    # it is because we are going to use inbuilt eval
    # it may result in very unexpected results for non valid
    # expressions
    for term in data:
        term.strip()

        # might result in blank strings
        if len(term) == 0:
            continue

        # checking that either term must be valid number
        # or a symbol, for symbol length cannot be greater
        # than 1
        try:
            float(term)

        except ValueError:
            if len(term) > 1:
                return 'error : please check input string'

    # after ensuring all safety running eval command
    try:
        answer = float(eval(message))

        # try to return integer
        if int(answer) == answer:
            return str(int(answer))

        # will return float as possible
        return str(answer)

    # giving error in case of division by 0
    except ZeroDivisionError:
        return 'error : division by 0 not allowed ' \
               '(getting 0 in denominator somewhere in expression)'

    # eval will not run on wrong expressions
    except:
        return 'error : please check input string'


# basic request handler
def handle_connection(connection, address):
    print(f'Connected with client socket number {address[0]}:{address[1]}')

    # while connection is there
    with connection:

        # accepting messages from client
        while True:

            # getting message as bytes (256)
            # decoding bytes to UTF-8
            # removing extra whitespaces received
            message = connection.recv(MAX_TRANSFER_SIZE).decode('utf-8').strip()

            # if no message is found then remove connection
            # possibly client disconnected
            if not message:
                break

            # printing message in desired format
            print(f'Client socket {address[0]}:{address[1]} sent the message: {message}')

            # calculating the answer
            answer = calculate(message)

            # printing answer in desired format
            print(f'Sending reply: {answer}')

            # encoding answers in bytes
            # sending to client
            connection.send(answer.encode('utf-8'))


"""
driver codes below it 
"""


# server driver
def server_driver():

    # starting TCP over IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # fixing port and host of the server
        server.bind((HOST, PORT))

        # listening on the port
        server.listen(0)

        # accepting connections, blocking query
        connection, address = server.accept()

        # closing for new TCP Connections
        server.close()

        # handling the data for each connection
        handle_connection(connection, address)

        # recursive calling for the next connection
        server_driver()


# for smooth handling of KeyBoardInterrupts
try:
    server_driver()

# handling KeyBoardInterrupt
except KeyboardInterrupt:
    sys.exit(1)
