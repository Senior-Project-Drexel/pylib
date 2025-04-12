from .client import Client


class RoundRobinClientManager:
    def __init__(self, addresses):
        self.next_client = 0

        self.clients = []
        for ip, port in addresses:
            self.clients.append(Client(ip, port))

    def client(self):
        client = self.clients[self.next_client]
        self.next_client = (self.next_client + 1) % len(self.clients)
        return client
