from socket import *
import sys
import time
import os

# Set the working directory to the directory containing the server file (Sesuain Sama Direktori File Server)
os.chdir('C:\Programming\Python Demo\TUBES JARKOM')

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket 
serverPort = 9999
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(5)
print('The server is ready to receive')

while True:
    # Establish the connection
    print("Ready to serve...")
    
    # Accept the connection
    connectionSocket, addr = serverSocket.accept()
    print(f'Connection received from: {addr}')

    print("Current working directory:", os.getcwd())
    try:
        start_time = time.time()  # Record the start time of request processing
        
        message = connectionSocket.recv(1024).decode()
        if not message:
            connectionSocket.close()
            continue  # Continue to the next iteration if the message is empty
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send HTTP header line into socket
        connectionSocket.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Send content of the requested file to the client
        connectionSocket.sendall(outputdata.encode())

        connectionSocket.close()

        end_time = time.time()  # Record the end time of request processing
        print(f"Request from {addr} processed in {end_time - start_time:.5f} seconds.")

    except IOError as e:
        print("IOError:", e)

        # Send response message for file not found
        connectionSocket.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    
        # Close client socket
        connectionSocket.close()

        end_time = time.time()  # Record the end time of request processing
        print(f"Request from {addr} failed: File not found. Processed in {end_time - start_time:.5f} seconds.")
    
serverSocket.close()
sys.exit()
