from typing import Tuple
import numpy as np

class Trust:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    async def matmul(self, a: np.ndarray, b: np.ndarray) -> Tuple[None, np.ndarray]:
        """Perform matrix multiplication without verification.
        
        Returns:
            Tuple[None, np.ndarray]: Always returns None for verification since this is a trust-based backend
        """
        client = self.client_manager.client()
        matrix_id = await client.send_matrix(a, b, op=0)
        c = await client.recv_matrix(matrix_id)
        return None, c
