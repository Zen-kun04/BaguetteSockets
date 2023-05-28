import socket
import threading
import time



def handle_client(client: socket.socket, packets: int):
    try:
        client.send(b"Hola xd")
        while client:
            if data := client.recv(packets).decode():
                print(data)
            else:
                break
    except ConnectionAbortedError:
        print('Conexión abortada por el cliente')
    except ConnectionResetError:
        print('Conexión restablecida por el cliente')

    finally:
        client.close()

def start_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 6666))
        sock.listen()
        print("Escuchando en el puerto 6666")
        
        while True:
            client, addr = sock.accept()
            print("Conexión establecida desde:", addr)

            client_thread = threading.Thread(target=handle_client, args=(client, 1024))
            client_thread.start()
            # time.sleep(2)
            # client.close()

    except KeyboardInterrupt:
        print("Interrupción de teclado detectada. Cerrando el programa...")

    finally:
        sock.close()

start_server()