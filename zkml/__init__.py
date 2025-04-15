import numpy as np

from . import backend, client

impl = None


async def matmul(a, b):
    assert isinstance(a, np.ndarray), "Numpy only"
    assert isinstance(b, np.ndarray), "Numpy only"

    if a.shape[1] != b.shape[0]:
        raise ValueError(
            "Incompatible dimensions for A*B. A has {a.shape[1]} columns, B has {b.shape[0]} rows."
        )

    c = await impl.matmul(a, b)
    return c
