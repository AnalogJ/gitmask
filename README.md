<p align="center">
  <a href="https://github.com/AnalogJ/gitmask">
  <img width="300" alt="gitmask_view" src="https://github.com/AnalogJ/gitmask/raw/beta/docs/noun_hacker_2481442.png">
  </a>
</p>

# Gitmask

Contribute Code Anonymously

# Introduction

Gitmask is an open source hosted service that allows you to contribute to Github projects anonymously.
It mimics a standard `git remote`, however all identifying information (author names, email and timestamps) embedded in
your commits are stripped, before forwarding a squashed commit to the target repository as a pull request.

# Features
- Does not require a Github account - Gitmask is completely anonymous
- Mimic's a standard git remote, allowing you to keep your normal development workflow and tools.
- Automatically creates a pull request against target repository & branch
- Hosted Open Source project. Use gitmask.com or run it yourself if you're privacy conscious.
- Inline progress logs
- **Coming Soon** Allows you to anonymously comment on Pull Requests opened by Gitmask, to provide context to your commits.


# Why?

There's a number of reasons why you may want to contribute to a Github project anonymously.

- Government - you may live in a country/region where the government tracks your [contributions online](https://en.wikipedia.org/wiki/Censorship_of_GitHub)
- Career - you may be contributing to a project that your employer may [not approve of](https://github.com/Cxbx-Reloaded/Cxbx-Reloaded)
- Security - you may want to contribute to a project that implies [financial interest](https://github.com/bitcoin/bitcoin)
- Prove a point - you may want to write something [controversial](https://github.com/offapi/rbac-23andme-oauth2) to start a discussion.
- You just value your privacy.


# Getting Started

```bash

git clone https://github.com/AnalogJ/gitmask.git
git checkout -b feat_branch
echo "update readme" >> README.md
git commit -am "Commits will be squashed and messages overwritten"
git remote add gitmask https://git.gitmask/v1/gh/AnalogJ/gitmask
git push gitmask feat_branch:master

# Gitmask will strip identifying information from your commits.
# You should see a link to the pull request that we open.

```

# Configuration

Coming Soon

# Testing

Coming Soon

# Contributing

Gitmask is written as a serverless project, specifically configured for the AWS Lambda Python runtime

You can run it locally by doing the the following:

- Create an AWS account where your gitmask run.
- Install nodejs, python, serverless-framework and aws-cli.
    - https://nodejs.org/
    - https://www.python.org
    - https://serverless.com/
    - https://aws.amazon.com/cli/
- Create and setup the AWS user for the deployment.
    - Set up the credentials with `aws configure`
    - You may use the AWS account root user.
    - You can create a new IAM user with restrict permissions.
       - https://serverless.com/blog/abcs-of-iam-permissions/ may help you.
- Issue your github access token
    - Go to github Settings > Developer settings > Personal access tokens
    - Run generate new token
       - scopes
          - public_repo

- Configure following environment variables:

    |Variable                 |Value  |
    |:------------------------|:-------------|
    |GITHUB_API_TOKEN         |github personal access token|
    |GITHUB_USER              |github username of the personal access token|
    |GITMASK_SERVICE          |Your own service name for gitmask, e.g. myown-gitmask-api.|
    |GITMASK_SERVICE_NORMALIZE|Normalized value for GITMASK_SERVICE,removing special characters and captalize the first letter. e.g. Myowngitmaskapi |
    |CIRCLE_SHA1              |Set the value retrieved by `git rev-parse --short HEAD`|

- Run deployment

    ```
    npm install -g serverless
    npm install
    pipenv install
    sls deploy
    ```

    * The URLs for endpoints are shown.
        * You can redisplay that with `sls info`


## Serverless offline

```
sls requirements install
PYTHONPATH=~/Library/Caches/serverless-python-requirements/2674a9f8121c5816727ff9f31e4684c72875956b15f0bbb0eb0d69838d6ad47b_slspyc sls offline start
```



## Useful Commands
- `GIT_TRACE=1 GIT_TRACE_PACKFILE=~/repos/gitmask/packfile.txt GIT_TRACE_CURL=2 GIT_CURL_VERBOSE=2 git push test beta2`
- `git unpack-objects -r < ~/repos/gitmask/packfile.txt`



# References

- https://janakiev.com/blog/python-shell-commands/
- https://mincong.io/2018/05/04/git-and-http/
- https://github.com/qhzhyt/http-git-server
- https://github.com/substack/git-http-backend
- https://github.com/asim/git-http-backend
- https://github.com/dvdotsenko/git_http_backend.py
- https://git-scm.com/book/no-nb/v1/Git-Internals-Transfer-Protocols
- https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols
- https://github.com/git/git/blob/master/Documentation/technical/http-protocol.txt
- https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols
- https://scottchacon.com/2010/03/04/smart-http.html
- https://github.com/schacon/grack/blob/master/lib/grack.rb
- https://mincong-h.github.io/2018/05/04/git-and-http/
- https://github.com/isomorphic-git/isomorphic-git/
- https://github.com/gabrielcsapo/node-git-server
- https://www.michaelfcollins3.me/blog/2012/05/18/implementing-a-git-http-server.html
- https://github.com/dulwich/dulwich/blob/aa73abcedb98ac469db645c4ac43ce2c2c6dd45f/dulwich/server.py#L893
- https://github.com/creationix/js-git/issues/3
- https://github.com/maxogden/git-side-band-message
- https://github.com/nhynes/git-angler/blob/master/lib/git_http_backend.js
- https://stackoverflow.com/questions/21833870/how-do-i-shallow-clone-a-repo-on-a-specific-branch
- https://github.com/lambci/git-lambda-layer
- https://github.com/serverless/serverless/blob/master/docs/providers/aws/guide/layers.md#using-your-layers
- https://github.com/Sneezoo/git-hapi-backend
- https://github.com/kisonecat/node-git-core
- https://github.com/chrisdickinson/git-packfile
- https://codewords.recurse.com/issues/three/unpacking-git-packfiles
- https://git-scm.com/docs/pack-format
- https://github.com/sosedoff/gitkit
- https://github.com/git/git/blob/master/builtin/receive-pack.c
- https://github.com/go-git/go-git/blob/c9533a6f9f3a6edd0fb7c8c161d4016a6af26bc3/storage/filesystem/dotgit/dotgit.go
- https://github.com/dulwich/dulwich
- http://weininger.net/configuration-of-nginx-for-gitweb-and-git-http-backend.html
- https://gist.github.com/massar/9399764
- https://stackoverflow.com/questions/22891148/nginx-how-to-run-a-shell-script-on-every-request
- https://github.com/markvnext/nginx-luarocks-docker/blob/master/nginx.sh
- https://git-scm.com/docs/git-http-backend
- https://apuntesderootblog.wordpress.com/2015/06/01/how-to-run-gitweb-and-git-http-backend-with-nginx-in-fedora/
- https://help.github.com/articles/changing-author-info/
- https://help.github.com/articles/pushing-to-a-remote/

# Logo

[hacker icon designed by sultan mohammed](https://thenounproject.com/term/hacker/2481442)
