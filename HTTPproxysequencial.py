from socket import *
import sys
import os

BASE_CACHE_DIR = "cache"

if not os.path.exists(BASE_CACHE_DIR):
    os.makedirs(BASE_CACHE_DIR)

def get_cache_path(host, path):
    host_dir = os.path.join(BASE_CACHE_DIR, host)
    if not os.path.exists(host_dir):
        os.makedirs(host_dir)

    full_path = os.path.join(host_dir, path.lstrip("/"))
    file_dir = os.path.dirname(full_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    return full_path

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


    cache_file = get_cache_path(host, path)
    if os.path.exists(cache_file):
        print(f"Cache hit for {full_url}")
        with open(cache_file, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client_socket.send(data)
        client_socket.close()
        return
    else:
        print(f"Cache miss for {full_url}")
        
    
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

    with open(cache_file, "wb") as f:
        while True:
            data = webSock.recv(4096)
            if not data:
                break
            f.write(data)
            client_socket.send(data)
    webSock.close()
    print('received reply from http server')
    print('reply forwarded to client')
    client_socket.close()


def proxyServer(portNo):
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(("0.0.0.0", portNo))
    tcpSerSock.listen(1)
    print('Ready to serve')
    while True:
        try:
            tcpCliSock, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)

            handle_client(tcpCliSock)
        except KeyboardInterrupt:
            print("proxy exiting!")
            tcpSerSock.close()
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 proxyServer.py proxyTCPPort")
        sys.exit(1)
    else:
        port = int(sys.argv[1])
        proxyServer(port)
