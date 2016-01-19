#!/usr/bin/env python
import os

print("Hook is running...")
print os.environ
#chmod -Rf u+w /srv/gitmask/username/repo.git/objects

# TODO: change the commiter email and name for all previous commits
# https://help.github.com/articles/changing-author-info/

# determine the repo that we need to fork
print('Destination Repository: ' + os.environ['GITHUB_DEST_REPO'])
print('Destination Branch: ' + os.environ['GITHUB_DEST_REPO'])

# TODO: validate that the destination repository hasn't been blocked for abuse

