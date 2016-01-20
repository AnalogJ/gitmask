#!/usr/bin/python -u
import os
import sys
import subprocess
import tempfile
import shutil
import time
from github3 import login


print("#### Gitmask is running...")
# determine the repo that we need to fork
dest_username = os.environ['GITHUB_DEST_USER']
dest_reponame = os.environ['GITHUB_DEST_REPO']
oldrev, newrev,  refname = [x.strip() for x in sys.stdin.read().split(' ')]

dest_branch = subprocess.check_output(["git", "rev-parse", "--symbolic", "--abbrev-ref", refname]).strip()

pull_request_url = None

print('Destination Repository: ' + dest_username + '/' + dest_reponame )
print('Destination Branch: ' + dest_branch + "(" + refname + ")")
print('Anonymous Commmits: ' + oldrev + '..' + newrev)


try:
    # TODO: validate that the destination repository hasn't been blocked for abuse

    print('#### Anonymize all new commits by replacing committer email address and name')
    # based off of http://stackoverflow.com/a/5018332/1157633
    # TODO: randomize commit timestamps as well?
    subprocess.check_output(["git", "filter-branch", "--tag-name-filter", "cat", "--env-filter",
                             "export GIT_AUTHOR_NAME='Anonymous'; export GIT_AUTHOR_EMAIL='gitmask-anonymous@users.noreply.github.com'; export GIT_COMMITTER_NAME='Anonymous'; export GIT_COMMITTER_EMAIL='gitmask-anonymous@users.noreply.github.com'"
                                , oldrev +".." +refname])

    # Authenticate against the github api
    token = os.environ['GITHUB_API_TOKEN']

    g = login(token=token)

    print('#### Forking the destination repository anonymously')
    remote_github_repository = g.repository(dest_username, dest_reponame)
    my_github_repository = remote_github_repository.create_fork()

    try:
        # add the upstream repo as a remote
        output = subprocess.check_output(["git", "remote", "add", "upstream", "https://"+token+"@github.com/"+my_github_repository.as_dict()['full_name']+".git"])

        print('#### Pushing local changes up github anonymously')
        output = subprocess.check_output(["git", "push", "upstream", dest_branch])
        time.sleep(5) # delays for 5 seconds

        print('#### Creating pull request')
        pull_request = remote_github_repository.create_pull('Test Title',dest_branch, 'gitmask-anonymous:'+refname)

        # print('#### Creating message on pr issue')
        # pull_request.create_comment()

        pull_request_url = pull_request.as_dict()['html_url']

    finally:
        print('#### Deleting forked repository')
        my_github_repository.delete()

finally:
    print('#### Cleaning up')
    shutil.rmtree(os.path.join(os.environ['GIT_PROJECT_ROOT'], dest_username))

    if pull_request_url:
        print('#### Your Pull Request is live: ' + pull_request_url)
    else:
        print('A pull request could not be created, check the logs.')

