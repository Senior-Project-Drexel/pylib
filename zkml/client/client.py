import asyncio
import zkml.proto.matrix_proto_pb2 as matrix_pb


class Client:
    matrix_id = 0

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    async def recv_matrix(self, id):
        if not self.reader:
            print("Error")

        len_bytes = await self.reader.readexactly(4)
        msg_len = int.from_bytes(len_bytes, byteorder="big")

        msg_bytes = await self.reader.readexactly(msg_len)
        matrix_msg = matrix_pb.MatrixMessage()  # type: ignore
        matrix_msg.ParseFromString(msg_bytes)

    async def send_matrix(self, a, b, op=0):
        if not self.writer:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

        cur_id = Client.matrix_id

        matrix1 = matrix_pb.Matrix()  # type: ignore
        matrix1.rols = a.shape[0]
        matrix1.cols = a.shape[1]
        matrix1.data.extend(a.flatten().tolist())

        matrix2 = matrix_pb.Matrix()  # type: ignore
        matrix2.rols = b.shape[0]
        matrix2.cols = b.shape[1]
        matrix2.data.extend(b.flatten().tolist())

        matrix_request = matrix_pb.MatrixRequest()  # type: ignore
        matrix_request.matrix1.CopyFrom(matrix1)
        matrix_request.matrix2.CopyFrom(matrix2)
        matrix_request.operation = op
        matrix_request.id = cur_id
        Client.matrix_id += 1

        serialized = matrix_request.SerializeToString()

        self.writer.write(len(serialized).to_bytes(4, byteorder="big"))
        self.writer.write(serialized)
        await self.writer.drain()

        return cur_id
