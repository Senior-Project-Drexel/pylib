import asyncio
import zkml.proto.matrix_proto_pb2 as matrix_pb


class Client:
    def __init__(self, ip, port):
        pass

    async def recv_matrix(self, id):
        if not self.reader:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

        len_bytes = await self.reader.readexactly(4)
        msg_len = int.from_bytes(len_bytes, byteorder="big")

        msg_bytes = await self.reader.readexactly(msg_len)
        matrix_msg = matrix_pb.MatrixMessage()  # type: ignore
        matrix_msg.ParseFromString(msg_bytes)

    async def send_matrix(self, m):
        matrix_msg = matrix_pb.MatrixMessage()  # type: ignore
        matrix_msg.rows = m.shape[0]
        matrix_msg.cols = m.shape[1]
        matrix_msg.data.extend(m.flatten().tolist())
        
        serialized = matrix_msg.SerializeToString()
        writer.write(len(serialized).to_bytes(4, byteorder='big'))
        writer.write(serialized)
        await writer.drain()
