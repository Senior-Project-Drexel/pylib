import numpy as np
from typing import Optional, Tuple

from . import backend, client

impl = None


async def matmul(a, b) -> np.ndarray:
    if not isinstance(a, np.ndarray):
        raise TypeError("a must be a numpy.ndarray")
    if not isinstance(b, np.ndarray):
        raise TypeError("b must be a numpy.ndarray")
    if a.shape[1] != b.shape[0]:
        raise ValueError(
            f"Incompatible dimensions for A*B. A has {a.shape[1]} columns, B has {b.shape[0]} rows."
        )

    verification_result, result = await impl.matmul(a, b)

    if verification_result is None:
        pass  # no verification was done
    if verification_result is False:
        raise RuntimeError("Matrix multiplication verification failed")

    return result
