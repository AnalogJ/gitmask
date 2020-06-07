from github import Github
from gitmask.lib.common.git import (repo_clone, repo_receive_pack, repo_checkout, repo_squash_commits, repo_push, repo_remote_add, repo_fetch)
from gitmask.lib.scm.github_utils import auth_remote_url
from gitmask.lib.gitmask_protocol import (inject, decode_branch)
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
        '                  https://www.gitmask.com                    ',
        '#############################################################'

    ]

    if event['isBase64Encoded']:
        body_bytes = base64.decodebytes(event['body'].encode('utf-8'))
    else:
        body_bytes = bytes(event['body'], 'utf-8')


    owner = event['pathParameters']['org']
    reponame = event['pathParameters']['repo'].replace('.git', '')

    messages.append(git_remote_message('Use git payload to determine which branch has been pushed'))
    branch = decode_branch(body_bytes)
    messages.append(git_remote_message('Pushed to: "{0}"'.format(branch)))

    scm_client = Github(GITHUB_API_TOKEN)
    origin_repo = scm_client.get_repo("{0}/{1}".format(owner, reponame))

    messages.append(git_remote_message('Validate target branch exists'))
    try:
        origin_repo.get_branch(branch)
    except:
        # TODO: wriite a valid error packet/protocol message that can be displayed via the git client UI.
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
            receive_pack_resp_bytes = repo_receive_pack(bare_git_repo, body_bytes)

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
                    title="Anonymous PR via Gitmask",
                    head="{0}:{1}".format(GITHUB_USER, anon_local_branch_name),
                    base=branch,
                    body='\n'.join([
                        'Hi!',
                        '',
                        'I\'m a bot for [gitmask.com](https://www.gitmask.com).',
                        '',
                        'I help developers protect their privacy, while still contributing to projects they love.',
                        'I do this by **removing identifying information** from their commits, **stripping commit messages** and **squashing** changes.',
                        'While these actions can make it harder for maintainers such as yourself to determine context for this PR, please consider that some of your users may not have the same freedoms that you enjoy.',
                        '',
                        'Gitmask is often a tool used out of necessity.',
                        '',
                        'If you are the contributor for this PR, you can go to the following url with your unique access token to respond to & comment on this PR anonymously',
                        '',
                        '[![Gitmask Messaging](https://img.shields.io/badge/Private%20Comment-%E2%96%BA-blue.svg)](https://www.gitmask.com/comment)',
                        '',
                        '---',
                        '',
                        'If you\'re interested in learning more about Gitmask, you can check it out [here](https://www.gitmask.com).'
                    ])
                )
                messages.append(git_remote_message('PR URL: {0}'.format(pr.html_url)))
                messages.append(git_remote_message('Delete forked repository'))
                gitmask_repo.delete()



    except:
        response_status_code = 500

    finally:
        resp_bytes = inject(receive_pack_resp_bytes, '\n'.join(messages).encode('utf-8'))

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
