import contextlib
import socket
import threading

listeners = {
    "ready": None,
    "connection": None,
    "message": None,
    "error": None
}

def on_ready(func):
    listeners["ready"] = func

def on_connection(func):
    listeners["connection"] = func

def on_message(func):
    listeners["message"] = func

def on_error(func):
    listeners["error"] = func

class BaguetteServerSockets():
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle(self, client: socket.socket, packets: int):
        try:
            while client and (data := client.recv(packets).decode()):
                if listeners["message"]:
                    listeners["message"](client, data)
        except ConnectionAbortedError:
            print('Conexión abortada por el cliente')
        except ConnectionResetError:
            print('Conexión restablecida por el cliente')

        finally:
            client.close()

    def listen(self, host: str = "localhost", port: str | int = 6666):
        """
        Server listener
        - :host: -> the host where the server will be listening to (localhost by default)
        - :port: -> the port where the server will be listening to (6666 by default)
        """
        if int(port) > 65535:
            if listeners["error"] is not None:
                listeners["error"]("Ports are between 0 and 65535")
            return
        self.sock.bind((host, port if type(port) == int else int(port)))
        self.sock.listen()
        if listeners["ready"]:
            listeners["ready"]()
        while 1:
            client, addr = self.sock.accept()
            if listeners["connection"]:
                listeners["connection"](client, addr)
            client_thread = threading.Thread(target=self.handle, args=(client, 1024))
            client_thread.start()

    def close_server(self):
        self.sock.close()
    
    def close_client(self, client: socket.socket):
        client.close()
    
    def send_message(self, client: socket.socket, message: str | bytes):
        if(type(message) == str):
            client.send(message.encode('utf-8'))
        else:
            client.send(message)

    

    