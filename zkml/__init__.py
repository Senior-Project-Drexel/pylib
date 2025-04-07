import numpy as np

import backend, client

impl = None


async def matmul(a, b):
    assert isinstance(a, np.ndarray), "Numpy only"
    assert isinstance(b, np.ndarray), "Numpy only"

    c = await impl.matmul(a, b)
    return c
