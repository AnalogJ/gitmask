from dulwich.server import (
    ReceivePackHandler,
    extract_capabilities
)
from dulwich.protocol import (  # noqa: F401
    CAPABILITY_AGENT,
    CAPABILITY_ATOMIC,
    CAPABILITIES_REF,
    CAPABILITY_DELETE_REFS,
    CAPABILITY_OFS_DELTA,
    CAPABILITY_QUIET,
    CAPABILITY_REPORT_STATUS,
    CAPABILITY_SIDE_BAND_64K,
    ZERO_SHA,
)

from dulwich.errors import (
    GitProtocolError
)

from typing import Iterable

# modified from ReceivePackHandler(PackHandler): https://github.com/dulwich/dulwich/blob/master/dulwich/server.py#L896
class GitmaskReceivePackHandler(ReceivePackHandler):
    """Protocol handler for downloading a pack from the client."""

    def __init__(self, backend, args, proto, http_req=None,
                 advertise_refs=False):
        super(GitmaskReceivePackHandler, self).__init__(
            backend, args, proto, http_req=http_req)
        self.repo = backend.open_repository(args[0])
        self.advertise_refs = advertise_refs

    @classmethod
    def capabilities(cls) -> Iterable[bytes]:
        return [
            CAPABILITY_REPORT_STATUS,
            CAPABILITY_DELETE_REFS,
            CAPABILITY_QUIET,
            CAPABILITY_ATOMIC,
            CAPABILITY_SIDE_BAND_64K
        ]


    def set_client_capabilities(self, caps: Iterable[bytes]) -> None:
        allowable_caps = set(self.innocuous_capabilities())
        allowable_caps.update(self.capabilities())
        for cap in caps:
            if cap.startswith(CAPABILITY_AGENT + b'='):
                continue
            if cap not in allowable_caps:
                raise GitProtocolError('Client asked for capability %r that '
                                       'was not advertised.' % cap)
        for cap in self.required_capabilities():
            if cap not in caps:
                raise GitProtocolError('Client does not support required '
                                       'capability %r.' % cap)
        self._client_capabilities = set(caps)
        # logger.info('Client capabilities: %s', caps)


    # modified from handle(self): https://github.com/dulwich/dulwich/blob/master/dulwich/server.py#L1001
    def handle_info_refs(self):
        refs = sorted(self.repo.get_refs().items())

        if not refs:
            refs = [(CAPABILITIES_REF, ZERO_SHA)]

        self.proto.write_pkt_line(b'# service=git-receive-pack\n')
        self.proto.write_pkt_line(None)
        self.proto.write_pkt_line(
        refs[0][1] + b' ' + refs[0][0] + b'\0' +
        self.capability_line(self.capabilities()) + b' agent=git/gitmask\n')

        for i in range(1, len(refs)):
            ref = refs[i]
            self.proto.write_pkt_line(ref[1] + b' ' + ref[0] + b'\n')
        self.proto.write_pkt_line(None)

    def handle_receive_pack(self):
        client_refs = []
        ref = self.proto.read_pkt_line()

        # if ref is none then client doesnt want to send us anything..
        if ref is None:
            return

        ref, caps = extract_capabilities(ref)
        self.set_client_capabilities(caps)

        # client will now send us a list of (oldsha, newsha, ref)
        while ref:
            client_refs.append(ref.split())
            ref = self.proto.read_pkt_line()

        # backend can now deal with this refs and read a pack using self.read
        status = self._apply_pack(client_refs)
        print("========status========")
        print(status)
        self._on_post_receive(client_refs)

        # when we have read all the pack from the client, send a status report
        # if the client asked for it
        if self.has_capability(CAPABILITY_REPORT_STATUS):
            self._report_status(status)
