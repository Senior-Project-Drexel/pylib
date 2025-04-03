import numpy as np
import zkml.proto.matrix_proto_pb2 as matrix_pb


async def send_matrix(m, writer):
    matrix_msg = matrix_pb.MatrixMessage()
    matrix_msg.rows = m.shape[0]
    matrix_msg.cols = m.shape[1]
    matrix_msg.data.extend(m.flatten().tolist())
    
    serialized = matrix_msg.SerializeToString()
    writer.write(len(serialized).to_bytes(4, byteorder='big'))
    writer.write(serialized)
    await writer.drain()

async def receive_matrix(reader):
    len_bytes = await reader.readexactly(4)
    msg_len = int.from_bytes(len_bytes, byteorder='big')
    
    msg_bytes = await reader.readexactly(msg_len)
    matrix_msg = matrix_pb.MatrixMessage()
    matrix_msg.ParseFromString(msg_bytes)

    # TODO:
    evidence = None
    
    return evidence, np.array(matrix_msg.data).reshape(matrix_msg.rows, matrix_msg.cols)