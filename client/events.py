import baguette_client_sockets as bcs


events = {
    "connection_success": bcs.on_connection_success,
    "message": bcs.on_message,
    "error": bcs.on_error
}

class EventDecorator:
    def __init__(self, event_name):
        self.event_name = event_name

    def __call__(self, function):
        if self.event_name in events:
            return events[self.event_name](function)

        return function

def event(event_name: str):
    """
    All socket events listed here:

    - `connection_success`: When a client connects successfully to a server.
    - `message`: When a client receives a message.
    """
    return EventDecorator(event_name)