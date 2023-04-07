import socket
import ssl
import threading
import dns.message
import struct
import os

DNS_HOST, DNS_PORT = '', 53
DoT_HOST, DoT_PORT = os.environ.get("DoT_HOST", "1.1.1.1"), 853

def handle_tcp(tcp_sock):
    while True:
        # Wait for a connection
         conn, tcp_addr = tcp_sock.accept()
         print('TCP Client connected:', tcp_addr)
         # Handle the connection
         request = conn.recv(1024)
         print('Received TCP request:', request)
         # connect to DoT server and get response
         response = DoT_connect(request)
         # Send a response back on the client's connection
         conn.sendall(response)
         # Close the connection
         conn.close()

def handle_udp(udp_sock):
    while True:
        # Handle the connection
        request, udp_addr = udp_sock.recvfrom(1024)
        print('Received UDP request:', request)

        # Create a DNS request message from the received bytes
        dns_request = dns.message.from_wire(request)
        # Convert the message to a bytes object
        request_bytes = dns_request.to_wire()
        # Add the length field to the message
        tcp_request = len(request_bytes).to_bytes(2, byteorder='big') + request_bytes
        # connect to DoT server and get response
        tcp_response = DoT_connect(tcp_request)
        # The DNS response is after the second byte
        dns_response = tcp_response[2:]
        # Extract the message ID from the original query
        query_id = struct.unpack('!H', request[:2])[0]
        # Set the message ID in the DNS response
        udp_response = struct.pack('!H', query_id) + dns_response[2:]
        # Send a response back to the client
        udp_sock.sendto(udp_response, udp_addr)

def DoT_connect(request):
    # Set up a socket for the DoT server and wrap it with SSL
    dot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = ssl.wrap_socket(dot_sock)
    # Connect to DoT server and get response
    wrappedSocket.connect((DoT_HOST, DoT_PORT))
    wrappedSocket.sendall(request)
    response = wrappedSocket.recv(1024)
    return response


# Set up a TCP socket for the DNS server
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((DNS_HOST, DNS_PORT))
tcp_sock.listen(2) # the server can listen to 2 clients simultaneously

# Set up a UDP socket for the DNS server
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((DNS_HOST, DNS_PORT))

t1 = threading.Thread(target=handle_tcp, args=(tcp_sock,))
t2 = threading.Thread(target=handle_udp, args=(udp_sock,))

print(f'Server listening on port {DNS_PORT}')

t1.start()
t2.start()

t1.join()
t2.join()
