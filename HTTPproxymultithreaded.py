from socket import *
import sys
import threading

def handle_client(client_socket):
    message = client_socket.recv(4096).decode()
    if not message:
        client_socket.close()
        return

    request_lines = message.split('\r\n')
    request_line = request_lines[0]
    try:
        method, full_url, http_version = request_line.split()
    except ValueError:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        return

    if method != "GET":
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        return

    http_pos = full_url.find("://")
    if http_pos == -1:
        host_path = full_url
    else:
        host_path = full_url[(http_pos + 3):]

    host, path = host_path.split("/", 1)
    path = "/" + path

    print('Connecting to original destination')
    try:
        webSock = socket(AF_INET, SOCK_STREAM)
        webSock.connect((host, 80))
        print('Connected to original destination')
        webSock.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())
    except Exception as e:
        print(f"Error connecting to server {host}: {e}")
        response = "HTTP/1.1 502 Bad Gateway\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        return

    while True:
        data = webSock.recv(4096)
        if not data:
            break
        client_socket.send(data)
    print('received reply from http server')
    webSock.close()
    print('reply forwarded to client')
    client_socket.close()

def proxyServer(portNo):
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(("0.0.0.0", portNo))

    tcpSerSock.listen(5)
    print('Ready to serve')

    while True:
        try:
            tcpCliSock, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)

            client_thread = threading.Thread(target=handle_client, args=(tcpCliSock,))
            client_thread.daemon = True
            client_thread.start()
        except KeyboardInterrupt:
            print("proxy exiting!")
            tcpSerSock.close()
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 proxyServer.py proxyTCPPort")
        sys.exit(1)
    else:
        port = int(sys.argv[1])
        proxyServer(port)
