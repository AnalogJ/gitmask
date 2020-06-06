from dulwich.protocol import Protocol
from gitmask.lib.scm.github_backend import GithubBackend
from gitmask.lib.gitmask_receive_pack_handler import GitmaskReceivePackHandler
import io

def handler(event, context):
    print(event)
    owner = event['pathParameters']['org']
    reponame = event['pathParameters']['repo'].replace('.git', '')

    # from receive_pack(path=".", inf=None, outf=None): https://github.com/dulwich/dulwich/blob/master/dulwich/porcelain.py#L1137
    repo_fullpath = "{0}/{1}".format(owner, reponame)

    inf = io.BytesIO()
    outf = io.BytesIO()

    backend = GithubBackend()

    def send_fn(data):
        outf.write(data)
        # outf.flush()

    proto = Protocol(inf.read, send_fn)
    handler = GitmaskReceivePackHandler(backend, [repo_fullpath], proto)
    handler.handle_info_refs()

    # send receive pack handler response to client

    response = {
        "statusCode": 200,
        "headers": {'Content-Type': "application/x-{0}-advertisement".format(event['queryStringParameters']['service'])},
        "body": outf.getvalue().decode("utf-8")
    }

    return response
