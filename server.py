import socket
import ssl
import os

DNS_HOST, DNS_PORT = '', 53
DoT_HOST, DoT_PORT = os.environ.get("DoT_HOST", "1.1.1.1"), 853

# Set up a socket for the local DNS proxy server
dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_sock.bind((DNS_HOST, DNS_PORT))
dns_sock.listen(2) # the server can listen to 2 clients simultaneously 

print('Server listening on port', DNS_PORT)

while True:
    try:
        # Wait for a connection
        conn, addr = dns_sock.accept()
        print('Client connected:', addr)

        # Receive the request
        request = conn.recv(1024)
        print('Received request:', request)
        
        # Set up a client socket with the DoT server and wrap it with SSL and connect
        dot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        wrappedSocket = ssl.wrap_socket(dot_sock)
        wrappedSocket.connect((DoT_HOST, DoT_PORT))

        # Send request on the DoT connection and receive reponse
        wrappedSocket.sendall(request)
        response = wrappedSocket.recv(1024)

        # Send a response back on the client's connection
        conn.sendall(response)

        # Close the connection
        conn.close()
    except Exception as e:
         # Handle any errors that occur during the connection
         print(f"Error occurred: {str(e)}")
