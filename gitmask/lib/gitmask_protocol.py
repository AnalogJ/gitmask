# inject data into
import io
from gitmask.lib.common.string import remove_prefix
from dulwich.protocol import (Protocol, pkt_line, SIDE_BAND_CHANNEL_PROGRESS)
from dulwich.server import (extract_capabilities, FileSystemBackend, ReceivePackHandler)

def inject(payload_bytes, inject_bytes):

    if payload_bytes.endswith(b'0000'):
        # the protocol payload has already been closed
        # we need to reopen it. Remove termination bytes
        payload_bytes = payload_bytes[:-4]


    resp_outf = io.BytesIO()
    def send_fn(data):
        resp_outf.write(data)

    resp_proto = Protocol(io.BytesIO().read, send_fn)

    resp_proto.write_sideband(SIDE_BAND_CHANNEL_PROGRESS, inject_bytes)

    # write termination block
    resp_proto.write_pkt_line(None)

    # append the new messages to the open payload
    return (payload_bytes + resp_outf.getvalue())


def decode_branch(payload_bytes):
    inf = io.BytesIO(payload_bytes)
    header_proto = Protocol(inf.read, lambda *args: None) #noop for output, we can ignore.
    ref, __ignore__ = extract_capabilities(header_proto.read_pkt_line())
    return remove_prefix(ref.decode("utf-8") .split(' ')[2], 'refs/heads/')
