import asyncio
import numpy as np
import zkml.proto.matrix_proto_pb2 as matrix_pb


class Client:
    matrix_id = 0

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self.pending_responses = {}  # {id, future}
        self.reader_task = None
        self._start_lock = asyncio.Lock()

    async def start(self):
        async with self._start_lock:
            if not self.reader_task:
                self.reader, self.writer = await asyncio.open_connection(
                    self.ip, self.port
                )
                self.reader_task = asyncio.create_task(self._reader_task())

    async def _reader_task(self):
        try:
            while True:
                if not self.reader:
                    raise RuntimeError("Reader is not initialized")
                len_bytes = await self.reader.readexactly(4)
                msg_len = int.from_bytes(len_bytes, byteorder="big")

                msg_bytes = await self.reader.readexactly(msg_len)
                response = matrix_pb.MatrixResponse()
                response.ParseFromString(msg_bytes)

                # Get the ID and find the waiting task
                response_id = response.id
                if response_id in self.pending_responses:
                    future = self.pending_responses.pop(response_id)
                    future.set_result(response)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            # If there's an error, cancel all pending responses
            for future in self.pending_responses.values():
                future.set_exception(e)
            self.pending_responses.clear()
            raise

    async def send_matrix(self, a, b, op=0):
        if not self.writer:
            await self.start()

        cur_id = Client.matrix_id

        matrix1 = matrix_pb.Matrix()
        matrix1.rows = a.shape[0]
        matrix1.cols = a.shape[1]
        matrix1.data.extend(a.flatten().tolist())

        matrix2 = matrix_pb.Matrix()
        matrix2.rows = b.shape[0]
        matrix2.cols = b.shape[1]
        matrix2.data.extend(b.flatten().tolist())

        matrix_request = matrix_pb.MatrixRequest()
        matrix_request.matrix1.CopyFrom(matrix1)
        matrix_request.matrix2.CopyFrom(matrix2)
        matrix_request.operation = op
        matrix_request.id = cur_id
        Client.matrix_id += 1

        serialized = matrix_request.SerializeToString()

        if not self.writer:
            raise RuntimeError("Writer is not initialized")

        self.writer.write(len(serialized).to_bytes(4, byteorder="big"))
        self.writer.write(serialized)
        await self.writer.drain()

        return cur_id

    async def recv_matrix(self, id):
        if not self.reader_task:
            await self.start()

        future = asyncio.Future()
        self.pending_responses[id] = future

        try:
            matrix_response = await future
            matrix_msg = matrix_response.matrix
            return np.array(matrix_msg.data).reshape(matrix_msg.rows, matrix_msg.cols)
        finally:
            self.pending_responses.pop(id, None)
