class Trust:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    # TODO: specify trust or freivalds
    async def matmul(self, a, b):
        client = self.client_manager.client()
        matrix_id = await client.send_matrix(a, b, op=0)
        c = await client.recv_matrix(matrix_id)
        e = None

        return e, c
