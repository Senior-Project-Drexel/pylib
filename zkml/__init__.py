import numpy as np

from . import protocol
from .client_manager import RoundRobinClientManager
from .verifier import NopVerifier

client_manager = None
verifier = None

async def init(addresses):
    global client_manager, verifier
    client_manager = RoundRobinClientManager(addresses)
    verifier = NopVerifier()
    await client_manager.ready()

async def matmul(a, b):
    assert isinstance(a, np.ndarray), "Numpy only"
    assert isinstance(b, np.ndarray), "Numpy only"

    reader, writer = client_manager.client()

    await protocol.send_matrix(a, writer) 
    await protocol.send_matrix(b, writer)
    evidence, c = await protocol.receive_matrix(reader)
    assert verifier.verify(evidence)
    return c