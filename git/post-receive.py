#!/usr/bin/python -u
import os
import sys
import subprocess
import tempfile
import shutil
from github3 import login


print("Hook is running...")
print os.environ
#chmod -Rf u+w /srv/gitmask/username/repo.git/objects

# determine the repo that we need to fork
dest_username = os.environ['GITHUB_DEST_USER']
dest_reponame = os.environ['GITHUB_DEST_REPO']
oldrev, newrev,  refname = sys.stdin.read().strip().split(' ')
dest_branch = subprocess.check_output(["git", "rev-parse", "--symbolic", "--abbrev-ref", refname]).strip()

print('Destination Repository: ' + dest_username + '/' + dest_reponame )
print('Destination Branch: ' + dest_branch)
print('Anonymous Commmits: ' + oldrev + '..' + newrev)

# TODO: validate that the destination repository hasn't been blocked for abuse

# TODO: change the commiter email and name for all commits between oldrev and newrev
#commits_between = subprocess.check_output(["git", "rev-list", oldrev+".."+newrev])
#commits = [s.strip() for s in commits_between.splitlines()]
#for commit in commits:
#    tmpdirname = tempfile.mkdtemp()
#    try:
#        subprocess.check_output(["git", "--work-tree="+tmpdirname,"rebase", "-i", commit, "-x","\"git commit --amend --author 'Anonymous User <darkmethod.z@gmail.com>' --no-edit\""])
#    finally:
#        shutil.rmtree(tmpdirname)

# based off of http://stackoverflow.com/a/5018332/1157633
subprocess.check_output(["git", "filter-branch", "--tag-name-filter", "cat", "--env-filter",
                         "export GIT_AUTHOR_NAME='Anonymous'; export GIT_AUTHOR_EMAIL='gitmask-automation@users.noreply.github.com'; export GIT_COMMITTER_NAME='Anonymous'; export GIT_COMMITTER_EMAIL='gitmask-automation@users.noreply.github.com'"
                            , oldrev +".." +refname])
#subprocess.check_output('git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d', shell=True)


# Authenticate against the github api
token = 'GITHUB_TOKEN'
g = login(token=token)

print('#### Forking the destination repository anonymously')
remote_github_repository = g.repository(dest_username, dest_reponame)
my_github_repository = remote_github_repository.create_fork()

# add the upstream repo as a remote
output = subprocess.check_output(["git", "remote", "add", "upstream", "https://"+token+"@github.com/"+my_github_repository.as_dict()['full_name']+".git"])

print('#### Pushing local changes up github anonymously')
output = subprocess.check_output(["git", "push", "upstream", dest_branch])

print('#### Creating pull request')
pull_request = remote_github_repository.create_pull('Test Title',dest_branch, 'gitmask-automation:'+dest_branch)

print('#### Creating message on pr issue')
pull_request.create_comment('This pull request was made on behalf of an anonymous user.')

print('#### Deleting forked repository')
my_github_repository.delete()

print('#### Cleaning up')
# TODO: delete local filesystem folders

