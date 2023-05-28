from events import event
from baguette_server_sockets import BaguetteServerSockets

@event("ready")
def on_ready():
    print("Servidor listo")

@event("connection")
def on_connection(client, addr):
    print("New connection from:", addr, "client:", client)
    bss.send_message(client, "Hola desde el servidor")

@event("message")
def on_message(client, message: str):
    print(f"Received new message from [{client}] =>", message)

bss = BaguetteServerSockets()
bss.listen()