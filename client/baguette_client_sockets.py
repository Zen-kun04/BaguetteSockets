import contextlib
import socket
import threading

listeners = {
    "connection_success": None,
    "message": None,
    "error": None
}

def on_connection_success(func):
    listeners["connection_success"] = func

def on_message(func):
    listeners["message"] = func

def on_error(func):
    listeners["error"] = func

class BaguetteClientSockets():
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host: str, port: str | int):
        """
        Connect to 
        """
        if int(port) > 65535:
            if listeners["error"] is not None:
                listeners["error"]("Ports are between 0 and 65535")
            return
        conn = self.sock.connect_ex((host, port if type(port) == int else int(port)))
        if not conn:
            listeners["connection_success"]()
            th = threading.Thread(target=self.recv)
            th.daemon = True
            th.start()
            with contextlib.suppress(KeyboardInterrupt):
                while True:
                    pass
        elif listeners["error"] is not None:
            listeners["error"](f"Could not connect to host => {host}:{port}")
    def close(self):
        self.sock.close()

    def recv(self):
        try:
            while True:
                if data := self.sock.recv(1024).decode():
                    listeners["message"](data)
                else:
                    break
        except ConnectionAbortedError:
            if listeners["error"] is not None:
                listeners["error"]("Connection has been lost")
        except ConnectionResetError:
            if listeners["error"] is not None:
                listeners["error"]("Server has been closed")
        finally:
            self.sock.close()
    
    def send_message(self, message: str | bytes):
        if(type(message) == str):
            self.sock.send(message.encode('utf-8'))
        else:
            self.sock.send(message)

    

    