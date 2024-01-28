# Example of a simple server
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5555))
server.listen(5)

while True:
    client, addr = server.accept()
    client.send(b"Hello, client!\n")
    client.close()


# Example using ZeroMQ as a message queue
# import zmq

# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555")

# while True:
#     message = input("Enter a message: ")
#     socket.send_string(message)
