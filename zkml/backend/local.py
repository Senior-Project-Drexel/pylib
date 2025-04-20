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

        m, n = a.shape  # a is m rows x n columns
        n_b, p = b.shape  # b is n_b rows x p columns

        if n != n_b:
            raise ValueError(
                f"Incompatible shapes for matrix multiplication: "
                f"{a.shape} and {b.shape}. Inner dimensions must match ({n} != {n_b})."
            )

        # --- Naive Multiplication ---
        # Initialize the result matrix 'c' with zeros.
        # It will have dimensions m x p.
        # Using lists first avoids needing np.zeros
        # for the core logic structure.
        c_list = [[0 for _ in range(p)] for _ in range(m)]

        # Iterate through rows of 'a' (index i)
        for i in range(m):
            # Iterate through columns of 'b' (index j)
            for j in range(p):
                # Compute the dot product for c[i][j]
                dot_product = 0
                # Iterate through columns of 'a' / rows of 'b' (index k)
                for k in range(n):  # or range(n_b) since n == n_b
                    dot_product += a[i, k] * b[k, j]
                # Assign the computed dot product to the result matrix element
                c_list[i][j] = dot_product

        # Convert the result list of lists back to a NumPy array
        # We try to match the input dtype if they are the same, otherwise default to float
        result_dtype = a.dtype if a.dtype == b.dtype else float
        c_np = np.array(c_list, dtype=result_dtype)

        return (None, c_np)
