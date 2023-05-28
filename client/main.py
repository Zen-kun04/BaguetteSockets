import baguette_client_sockets as bcs
from baguette_client_sockets import BaguetteClientSockets
from events import event


@event("connection_success")
def on_connection_success():
    print("Cliente conectado correctamente")

@event("message")
def on_message(message):
    print("Mensaje:", message)
    s.send_message("Hola bro")

@event("error")
def on_error(err):
    print("Error:", err)


s = BaguetteClientSockets()
s.connect('localhost', 6666)