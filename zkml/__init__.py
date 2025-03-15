import asyncio
import struct
import numpy as np

clients = []
next_client = 0

async def init(addresses):
    for ip, port in addresses:
        clients.append(await asyncio.open_connection(ip, port))

async def send_matrix(m, writer):
    r, c = m.shape
    writer.write(struct.pack(">I", r))
    writer.write(struct.pack(">I", c))
    for e in m.flatten():
        writer.write(struct.pack(">I", e))
    await writer.drain()

async def receive_matrix(reader):
    left = None
    num = []

    while True:
        buf = await reader.read(1024)
        n = len(buf) // 4
        r = len(buf) % 4

        for i in range(0, n):
            n, = struct.unpack(">I", buf[i * 4:(i + 1) * 4])
            num.append(n)

        if len(num) < 2 or len(num) != num[0] * num[1] + 2:
            continue

        return np.array(num[2:]).reshape(num[0], num[1])

async def matmul(m1, m2):
    assert isinstance(m1, np.ndarray), "Numpy only"
    assert isinstance(m2, np.ndarray), "Numpy only"

    global next_client
    reader, writer = clients[next_client]
    next_client = next_client + 1 % len(clients)

    await send_matrix(m1, writer) 
    await send_matrix(m2, writer)
    return await receive_matrix(reader)