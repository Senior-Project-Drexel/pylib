import numpy as np

from . import protocol
from .config import Config

config = Config()

async def init(addresses, backend=None, verifier=None, client_manager=None):
    config.configure(addresses, backend, verifier, client_manager)
    client_manager = config.client_manager_instance()
    await client_manager.ready()

async def matmul(a, b):
    assert isinstance(a, np.ndarray), "Numpy only"
    assert isinstance(b, np.ndarray), "Numpy only"

    backend = config.backend_instance()
    return backend.matmul()

    # this is remote backend code
    reader, writer = client_manager.client()
    await protocol.send_matrix(a, writer)
    await protocol.send_matrix(b, writer)
    evidence, c = await protocol.receive_matrix(reader)
    assert verifier.verify(evidence)

    return c