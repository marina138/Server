import socket
import sys


def send_request(proxy_host, proxy_port, url):
    request = f"GET {url} HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((proxy_host, proxy_port))
        client_socket.sendall(request.encode())

        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data

    return response.decode()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <proxy_host> <proxy_port> <url>")
        sys.exit(1)

    proxy_host = sys.argv[1]
    proxy_port = int(sys.argv[2])
    url = sys.argv[3]

    response = send_request(proxy_host, proxy_port, url)
    print(response)
