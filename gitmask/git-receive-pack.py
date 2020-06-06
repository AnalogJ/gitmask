from dulwich.protocol import (Protocol, pkt_line, SIDE_BAND_CHANNEL_PROGRESS)
from dulwich.server import (extract_capabilities, FileSystemBackend, ReceivePackHandler)
from github import Github
from gitmask.lib.common.git import (repo_clone, repo_checkout, repo_squash_commits, repo_push, repo_remote_add, repo_fetch)
from gitmask.lib.common.string import remove_prefix
from gitmask.lib.scm.github_utils import auth_remote_url
from gitmask.lib.gitmask_protocol import inject
import io
import tempfile
import os
import subprocess
import base64
import uuid

GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
GITHUB_USER = os.environ.get('GITHUB_USER')

# from receive_pack(path=".", inf=None, outf=None): https://github.com/dulwich/dulwich/blob/master/dulwich/porcelain.py#L1137
def handler(event, context):
    print(event)

    messages = [
        '#############################################################',
        '         d8b 888                                    888      ',
        '         Y8P 888                                    888      ',
        '             888                                    888      ',
        ' .d88b.  888 888888 88888b.d88b.   8888b.  .d8888b  888  888 ',
        'd88P"88b 888 888    888 "888 "88b     "88b 88K      888 .88P ',
        '888  888 888 888    888  888  888 .d888888 "Y8888b. 888888K  ',
        'Y88b 888 888 Y88b.  888  888  888 888  888      X88 888 "88b ',
        ' "Y88888 888  "Y888 888  888  888 "Y888888  88888P" 888  888 ',
        '     888                                                     ',
        'Y8b d88P                                                     ',
        ' "Y88P"                                                      ',
        '                       www.gitmask.com                       ',
        '#############################################################'

    ]

    if event['isBase64Encoded']:
        body_bytes = base64.decodebytes(event['body'].encode('utf-8'))
    else:
        body_bytes = bytes(event['body'], 'utf-8')
    inf = io.BytesIO(body_bytes)
    outf = io.BytesIO()

    owner = event['pathParameters']['org']
    reponame = event['pathParameters']['repo'].replace('.git', '')

    messages.append(git_remote_message('Use git payload to determine which branch has been pushed'))
    headerProto = Protocol(inf.read, lambda *args: None) #noop for output, we can ignore.
    ref, __ignore__ = extract_capabilities(headerProto.read_pkt_line())
    branch = remove_prefix(ref.decode("utf-8") .split(' ')[2], 'refs/heads/')
    messages.append(git_remote_message('Pushed to: "{0}"'.format(branch)))

    scm_client = Github(GITHUB_API_TOKEN)
    origin_repo = scm_client.get_repo("{0}/{1}".format(owner, reponame))

    messages.append(git_remote_message('Validate target branch exists'))
    try:
        origin_repo.get_branch(branch)
    except:
        return {
            "statusCode": 400,
            "headers": {'Content-Type': "application/x-git-receive-pack-result"},
            "body": 'Branch "{0}" does not exist on target repo "{1}/{2}". Try `git push gitmask local_branch:target_branch`'.format(branch, owner, reponame)
        }

    messages.append(git_remote_message('Fork "{0}/{1}" anonymously on github'.format(owner, reponame)))
    gitmask_repo = origin_repo.create_fork()

    response_status_code = 200
    try:

        with tempfile.TemporaryDirectory(dir='/tmp') as bare_git_repo:

            messages.append(git_remote_message('Clone the forked repository locally'))
            authremote = auth_remote_url(GITHUB_API_TOKEN, GITHUB_USER, reponame)
            repo_clone(authremote, bare_git_repo, True)
            repo_fetch(bare_git_repo)

            messages.append(git_remote_message('Apply the git payload to the specified branch'))
            env = os.environ.copy()
            # env['GIT_TRACE'] = '1'
            p = subprocess.Popen(['git-receive-pack', "--stateless-rpc", bare_git_repo], cwd=bare_git_repo, env=env, stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)

            p.stdin.write(body_bytes)
            p.stdin.flush()

            for line in p.stdout:
                outf.write(line)

            with tempfile.TemporaryDirectory(dir='/tmp') as full_git_repo:
                messages.append(git_remote_message('Creating working-tree'))

                repo_clone(bare_git_repo, full_git_repo)
                repo_remote_add(full_git_repo, 'upstream', authremote)
                repo_fetch(full_git_repo)

                messages.append(git_remote_message('Squashing commits to an anonymous branch'))
                anon_local_branch_name = "gitmask-{0}".format(uuid.uuid4())
                repo_squash_commits(
                    full_git_repo,
                    "upstream/{0}".format(branch), # dest_branch
                    anon_local_branch_name, # squashed_branch
                    'origin/{0}'.format(branch) # packfile_branch
                )

                messages.append(git_remote_message('Pushing anonymous branch up to forked repository'))
                repo_push(full_git_repo, 'upstream', anon_local_branch_name)

                messages.append(git_remote_message('Opening a PR against target repository & branch'))
                pr = origin_repo.create_pull(
                    title="Gitmask Anonymous PR",
                    body="This is an anonymous PR submitted via Gitmask - https://www.gitmask.com",
                    head="{0}:{1}".format(GITHUB_USER, anon_local_branch_name),
                    base=branch
                )
                messages.append(git_remote_message('PR URL: {0}'.format(pr.html_url)))
                messages.append(git_remote_message('Delete forked repository'))
                gitmask_repo.delete()



    except:
        response_status_code = 500

    finally:
        resp_bytes = inject(outf.getvalue(), '\n'.join(messages).encode('utf-8'))

        messages.append(git_remote_message('error: cleanup forked repository'))
        try:
            gitmask_repo.delete()
        except:
            pass

    response = {
        "statusCode": response_status_code,
        "headers": {'Content-Type': "application/x-git-receive-pack-result"},
        "body": resp_bytes.decode("utf-8")
    }

    print("======> Response:", response)
    return response

def git_remote_message(message):
    print(message)
    return message
