import socket
import sys
import urllib.parse
import msvcrt

def fetch(url):
    parsed_url = urllib.parse.urlparse(url) #разбор юрл на части
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 80
    path = parsed_url.path if parsed_url.path else '/'
    if parsed_url.query:
        path += '?' + parsed_url.query

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # Создает TCP-сокет
        sock.connect((host, port)) #Подключается
        sock.sendall(request.encode()) #Отправляет HTTP-запрос серверу.

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

    return response.decode()

def display_content(content):
    lines = content.splitlines() #Разбивает содержимое ответа на строки.
    index = 0 #Инициализирует начальный индекс строки.
    page_size = 25 #Определяет количество строк, отображаемых на одной странице.

    while index < len(lines):
        end_index = min(index + page_size, len(lines)) #Вычисляет индекс конца текущей страницы.
        for line in lines[index:end_index]:
            print(line)
        index = end_index #Обновляет начальный индекс для следующей страницы.

        if index < len(lines):
            print("\nPress space to scroll down...")

            while True:
                if msvcrt.kbhit(): #кливиша нажата
                    key = msvcrt.getch() #считывает
                    if key == b' ': # вывоод старинцы
                        break

if __name__ == "__main__":
    if len(sys.argv) != 2: #['http_client.py', 'http://example.com']
        print("Usage: python http_client.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    response = fetch(url) #Делает HTTP-запрос и получает ответ.

    header_end = response.find('\r\n\r\n') #Находит конец заголовков HTTP-ответа.
    body = response[header_end+4:] #Извлекает тело ответа (данные после заголовков)

    display_content(body)
