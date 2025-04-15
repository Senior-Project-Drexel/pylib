import numpy as np


class Freivalds:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    def _verify(self, A, B, C, k=5):
        for _ in range(k):
            r = np.random.randint(
                0, 2, size=(B.shape[1], 1), dtype=np.int64
            )  # using int64 to avoid potential overflow on large sums
            Br = B @ r
            A_Br = A @ Br
            Cr = C @ r

            if not np.array_equal(A_Br, Cr):
                return False

        return True

    # TODO: specify trust or freivalds
    async def matmul(self, a, b):
        client = self.client_manager.client()
        await client.send_matrix(a)
        await client.send_matrix(b)
        c = await client.recv_matrix()
        e = self._verify(a, b, c)

        return e, c
