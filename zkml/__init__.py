import numpy as np

from .config import Config

cfg = Config()


async def init(addresses=None, backend=None, verifier=None, client_manager=None):
    cfg.configure(addresses, backend, verifier, client_manager)
    client_manager = cfg.client_manager_instance()
    await client_manager.ready()


async def matmul(a, b):
    assert isinstance(a, np.ndarray), "Numpy only"
    assert isinstance(b, np.ndarray), "Numpy only"

    backend = cfg.backend_instance()
    c = await backend.matmul(a, b)
    return c


def configure(addresses=None, backend=None, verifier=None, client_manager=None):
    cfg.configure(addresses, backend, verifier, client_manager)
