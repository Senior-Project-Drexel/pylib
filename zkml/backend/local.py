from typing import Tuple
import numpy as np


class Local:
    def __init__(self):
        pass

    async def matmul(self, a: np.ndarray, b: np.ndarray) -> Tuple[None, np.ndarray]:
        """Perform matrix multiplication locally without verification.

        Returns:
            Tuple[None, np.ndarray]: Always returns None for verification since this is a local computation
        """
        c = a @ b
        return None, np.array(c).reshape(c.shape[0], c.shape[1])
