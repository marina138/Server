import socket
import select
import sys

cache = {}


def handle_request(client_socket):
    request = client_socket.recv(4096) #Получает запрос от клиента.
    if not request: #Если запрос пустой
        return

    # Извлечение первой строки из запроса
    first_line = request.decode().split('\n')[0]
    url = first_line.split(' ')[1]

    if url in cache:
        print("Found in cache:", url)
        client_socket.sendall(cache[url])
    else:
        print("Not found in cache, fetching from server:", url)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #Создает сокет для подключения к серверу.
            server_socket.connect(('www.example.com', 80)) #подключение к серверу
            server_socket.sendall(request)#отправка запроса
            response = server_socket.recv(4096)#получение ответа
            client_socket.sendall(response)#ответ клиенту
            cache[url] = response


def start_proxy_server(listen_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Создает TCP-сокет
    # Устанавливает опцию сокета, позволяющую повторно использовать локальный адрес.
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('127.0.0.1', listen_port))
    proxy_socket.listen(5)
    print("Proxy server is listening on port", listen_port)

    while True:
        readable, _, _ = select.select([proxy_socket], [], []) #Ожидание событий ввода/вывода на сокете.
        for sock in readable:
            if sock == proxy_socket: #Если готовый сокет — это прокси-серверный сокет:
                client_socket, _ = proxy_socket.accept() #ринимает новое входящее соединение.
                print("Accepted connection from", client_socket.getpeername())
                handle_request(client_socket)
                client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python proxy_server.py <port>")
        sys.exit(1)

    listen_port = int(sys.argv[1]) #Преобразует аргумент командной строки в целое число (порт).
    start_proxy_server(listen_port) #Запускает прокси-сервер на указанном порту.
