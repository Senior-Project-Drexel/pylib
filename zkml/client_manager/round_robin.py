import asyncio

class RoundRobinClientManager:
    def __init__(self, addresses):
        self.addresses = addresses
        self.next_client = 0

        self.futures = []
        for ip, port in addresses:
            self.futures.append(asyncio.open_connection(ip, port))

    async def ready(self):
        self.clients = await asyncio.gather(*self.futures)

    def client(self):
        client = self.clients[self.next_client]
        self.next_client = self.next_client + 1 % len(self.clients)
        return client