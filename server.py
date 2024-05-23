import selectors
import socket
import types
#ввод/вывод
sel = selectors.DefaultSelector()


def accept_connect(socket):
    conect, addClient = socket.accept()
    print(f'Соединение от {addClient}')
    conect.setblocking(False)#: Устанавливает неблокирующий режим для сокета.
    data = types.SimpleNamespace(addr=addClient, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #отслеживания чтения или записи
    sel.register(conect, events, data=data) # Регистрирует сокет в селекторе для отслеживания указанных событий и связывает с ним объект data.

def service_connection(key, mask):
    sock = key.fileobj #Получает объект сокета
    data = key.data #Получает объект data, связанный с сокетом.
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data # то в буфер
        else:
            print(f'Закрытие соединения с {data.addClient}')
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb) #количество байтов
            data.outb = data.outb[sent:]


if __name__ == '__main__':
    host, port = 'localhost', 9090
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создает объект сокета для TCP-соединений с IPv4-адресами.
    lsock.bind((host, port)) #привязка
    lsock.listen()
    print(f'Сервер запущен на {host}:{port}')
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_connect(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print('Сервер остановлен')
    finally:
        sel.close()
