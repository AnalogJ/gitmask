from dulwich.porcelain import (clone, pull, update_head, branch_list, active_branch)
import subprocess
import os

def repo_clone(git_remote, repo_path, is_bare=False):
    # '--depth', '1',

    cmd = ['git', 'clone']
    if is_bare:
        cmd.append('--bare')
    cmd.append(git_remote)
    cmd.append(repo_path)

    process = subprocess.check_call(cmd)


def repo_fetch(repo_path):
    process_fetch = subprocess.check_call(['git', 'fetch', '--all'], cwd=repo_path)

def repo_checkout(repo_path, branch_name):
    process = subprocess.check_call(['git', 'checkout', branch_name], cwd=repo_path)

def repo_squash_commits(repo_path, dest_branch, squashed_branch, packfile_branch):

    process = subprocess.check_call(['git', 'checkout', '-b', squashed_branch, dest_branch], cwd=repo_path)

    process_merge = subprocess.check_call(['git', 'merge', '--squash', packfile_branch], cwd=repo_path)

    cust_env = os.environ.copy()
    cust_env['GIT_COMMITTER_NAME'] = 'ghost'
    cust_env['GIT_COMMITTER_EMAIL'] = 'ghost@users.noreply.github.com'
    cust_env['GIT_AUTHOR_NAME'] = 'ghost'
    cust_env['GIT_AUTHOR_EMAIL'] = 'ghost@users.noreply.github.com'

    # make a squashed commit on the squashed_branch
    process_add = subprocess.check_call(['git', 'commit', '-am', 'gitmask.com anonymous commit'], cwd=repo_path, env=cust_env)


def repo_push(repo_path, remote_name, branch_name):
    process = subprocess.check_call(['git', 'push', remote_name, branch_name], cwd=repo_path)

def repo_remote_add(repo_path, remote_name, remote_url):
    process = subprocess.check_call(['git', 'remote', 'add', remote_name, remote_url], cwd=repo_path)


#
#
# def clone_repo(gitRemote, destination, branch, depth=1):
#     branch_ref = bytes('refs/heads/{0}'.format(branch), 'utf-8')
#
#     local_repo = clone(gitRemote, destination, bare=False)
#     pull(destination, refspecs=[b'HEAD', branch_ref])
#
#     print("=====AFTER=====>", branch_list(destination))
#     update_head(destination, branch_ref, False)
#     local_repo.reset_index(local_repo[branch_ref].tree)
#     local_repo.refs.set_symbolic_ref(b'HEAD', branch_ref)
#     print("ACTIVE BRANCH====>", active_branch(destination))

# def checkout_branch(repoPath, branchName):
#     return execGitCmd(`git checkout ${branchName}`, repoPath)

