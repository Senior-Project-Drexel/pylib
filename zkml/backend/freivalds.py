class Freivalds:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    # TODO: specify trust or freivalds
    async def matmul(self, a, b):
        client = self.client_manager.client()
        await client.send_matrix(a)
        await client.send_matrix(b)
        evidence, c = await client.recv_matrix()

        return c
