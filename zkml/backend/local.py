import numpy as np


class Local:
    def __init__(self):
        pass

    async def matmul(self, a: np.ndarray, b: np.ndarray):
        c = a @ b
        e = None
        return e, np.array(c).reshape(c.shape[0], c.shape[1])
