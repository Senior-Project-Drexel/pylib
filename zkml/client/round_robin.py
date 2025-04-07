import asyncio

from zkml.client import Client


class RoundRobinClientManager:
    def __init__(self, addresses):
        self.addresses = addresses
        self.next_client = 0

        self.futures = []
        for ip, port in addresses:
            self.futures.append(Client(ip, port))

    def client(self):
        client = self.clients[self.next_client]
        self.next_client = self.next_client + 1 % len(self.clients)
        return client
