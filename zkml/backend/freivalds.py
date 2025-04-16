from typing import Tuple
import numpy as np


class Freivalds:
    def __init__(self, client_manager):
        self.client_manager = client_manager

    def _verify(self, A: np.ndarray, B: np.ndarray, C: np.ndarray, k: int = 5) -> bool:
        """Verify matrix multiplication using Freivalds algorithm.
        
        Args:
            k: Number of verification rounds. Higher k increases verification confidence.
        
        Returns:
            bool: True if verification passed, False if verification failed
        """
        for _ in range(k):
            r = np.random.randint(
                0, 2, size=(B.shape[1], 1), dtype=np.int64
            )  # using int64 to avoid potential overflow on large sums
            Br = B @ r
            A_Br = A @ Br
            Cr = C @ r

            if not np.allclose(A_Br, Cr):
                print("Error: Verification failed")
                return False

        return True

    async def matmul(self, a: np.ndarray, b: np.ndarray) -> Tuple[bool, np.ndarray]:
        """Perform matrix multiplication with Freivalds verification.
        
        Returns:
            Tuple[bool, np.ndarray]: (verification_result, result) where verification_result
            is True if verification passed, False if verification failed
        """
        client = self.client_manager.client()
        matrix_id = await client.send_matrix(a, b, op=0)
        c = await client.recv_matrix(matrix_id)
        verification_result = self._verify(a, b, c)

        return verification_result, c
