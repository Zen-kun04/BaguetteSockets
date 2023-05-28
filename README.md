# **BaguetteSockets**

I've made BaguetteSockets to make it easier socket developing. So let's say you want to create a project that use sockets, then you can use BaguetteSockets.

With less than 20 lines of code you can create a fully functional server that will:
- listen for new connections
- detect incomming connections
- detect received messages
- send messages when it received one from a client

And with less than 20 lines of code you can also make your basic client !
- connect to a server
- detect successfull connection
- detect messages sent by the server
- support errors (print them just in case)

## Code examples:

**Server:**
```python
from events import event
from baguette_server_sockets import BaguetteServerSockets

@event("ready")
def on_ready():
    print("Server ready")

@event("connection")
def on_connection(client, addr):
    print("New connection from:", addr, "client:", client)
    bss.send_message(client, "Hi from the server !")

@event("message")
def on_message(client, message: str):
    print(f"Received new message from [{client}] =>", message)

bss = BaguetteServerSockets()
bss.listen("localhost", 1234) # By default it will connect to localhost:6666
```

**Client:**
```python
from baguette_client_sockets import BaguetteClientSockets
from events import event

@event("connection_success")
def on_connection_success():
    print("Successfully connected to server")

@event("message")
def on_message(message):
    print("Message from server:", message)
    s.send_message("Hi, this is the client ^^")

@event("error")
def on_error(err):
    print("Error:", err)

s = BaguetteClientSockets()
s.connect('localhost', 6666)
```