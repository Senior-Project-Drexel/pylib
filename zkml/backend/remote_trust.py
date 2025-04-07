from zkml import cfg, protocol


class RemoteTrust:
    def __init__(self):
        pass

    # TODO: specify trust or freivalds
    async def matmul(self, a, b):
        cm = cfg.client_manager_instance()

        reader, writer = cm.client()
        await protocol.send_matrix(a, writer)
        await protocol.send_matrix(b, writer)
        evidence, c = await protocol.receive_matrix(reader)

        return c
