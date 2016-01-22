#!/usr/bin/python -u
import os
import subprocess
import stat
import shutil
import grp

# check if the requested git repository exists.
requestrepo = os.environ['REQUEST_URI'].split('.git')[0]
username, reponame = requestrepo.lstrip('/').split('/')
userpath = os.path.join(os.environ['GIT_PROJECT_ROOT'], username)
repopath = os.path.join(userpath, reponame + '.git')

if not os.path.isdir(repopath):
    # create an empty git repo
    os.makedirs(repopath)
    os.chdir(repopath)

    # set the correct git options
    output = subprocess.check_output(["git", "clone", "--bare", "https://github.com/" + username + '/' + reponame + '.git', repopath])
    output = subprocess.check_output(["git", "config", "http.receivepack", "true"])
    output = subprocess.check_output(["git", "config", "core.sharedRepository", "true"])

    # copy over the post-receive hook & make executable
    hookpath = os.path.join(repopath, 'hooks/post-receive')
    shutil.copy('/srv/gitmask/post-receive.py', hookpath)
    st = os.stat(hookpath)
    os.chmod(hookpath, st.st_mode | stat.S_IEXEC)

    # setup permissions
    #gitinfo = grp.getgrnam('git')
    wwwdatainfo = grp.getgrnam('www-data')

    for root, dirs, files in os.walk(userpath):
        os.chown(root, wwwdatainfo.gr_gid, wwwdatainfo.gr_gid)
        st = os.stat(root)
        os.chmod(root, st.st_mode | stat.S_IRGRP | stat.S_IWGRP | stat.S_ISGID)


httpbackendcmd = ["/usr/lib/git-core/git-http-backend"]

childenv = {'PATH_INFO': os.environ['PATH_INFO'],
            'GIT_HTTP_EXPORT_ALL': '',
            'GIT_PROJECT_ROOT': os.environ['GIT_PROJECT_ROOT'],
            'REMOTE_USER': 'anonymous',
            'REMOTE_ADDR': 'gitmask.com',
            'CONTENT_TYPE': os.environ['CONTENT_TYPE'],
            'QUERY_STRING': os.environ['QUERY_STRING'],
            'REQUEST_METHOD': os.environ['REQUEST_METHOD'],
            'GITHUB_DEST_USER': username,
            'GITHUB_DEST_REPO': reponame,
            'GITHUB_API_TOKEN': os.environ['GITHUB_API_TOKEN']
            }

process = subprocess.Popen(httpbackendcmd, shell=False,
                           #stdout=subprocess.STDOUT,
                           #stderr=subprocess.STDERR,
                           env=childenv)

# wait for the process to terminate
out, err = process.communicate()
errcode = process.returncode

# print("Content-type:text/html\r\n")
# print("<html><head>")
# print("<title>test</title>")
# print('<meta name="description" content="test">')
# print('<meta name="keywords" content="test">')
# print('<meta http-equiv="Content-type" content="text/html;charset=UTF-8">')
# print('<meta name="ROBOTS" content="noindex">')
# print("</head><body><pre>")
# print os.environ
# print("</pre></body></html>")
