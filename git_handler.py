#!/usr/bin/env python
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
    output = subprocess.check_output(["git", "init", "--bare", repopath])
    output = subprocess.check_output(["git", "config", "http.receivepack", "true"])
    output = subprocess.check_output(["git", "config", "core.sharedRepository", "true"])

    # copy over the post-receive hook & make executable
    hookpath = os.path.join(repopath,'hooks/post-receive')
    shutil.copy('/srv/gitmask/post-receive.hook', hookpath)
    st = os.stat(hookpath)
    os.chmod(hookpath, st.st_mode | stat.S_IEXEC)

    # setup permissions
    #gitinfo = grp.getgrnam('git')
    wwwdatainfo = grp.getgrnam('www-data')

    for root, dirs, files in os.walk(userpath):
        os.chown(root, wwwdatainfo.gr_gid, wwwdatainfo.gr_gid)
        st = os.stat(root)
        os.chmod(root, st.st_mode | stat.S_IRGRP | stat.S_IWGRP | stat.S_ISGID)



print("Content-type:text/html\r\n")
print("<html><head>")
print("<title>test</title>")
print('<meta name="description" content="test">')
print('<meta name="keywords" content="test">')
print('<meta http-equiv="Content-type" content="text/html;charset=UTF-8">')
print('<meta name="ROBOTS" content="noindex">')
print("</head><body><pre>")
print os.environ
print("</pre></body></html>")
