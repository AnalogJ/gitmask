<p align="center">
  <a href="https://github.com/AnalogJ/gitmask">
  <img width="300" alt="gitmask_view" src="https://github.com/AnalogJ/gitmask/raw/beta/docs/noun_hacker_2481442.png">
  </a>
</p>

# Gitmask **Work-In-Progress**


HELLO WORLD



# Contributing


```
pipenv install packge_name
pipenv run pip freeze > requirements.txt

sls requirements install
PYTHONPATH=/Users/jason/Library/Caches/serverless-python-requirements/2674a9f8121c5816727ff9f31e4684c72875956b15f0bbb0eb0d69838d6ad47b_slspyc sls offline start


```

# Applying test packfile
```
 GIT_TRACE=1 GIT_TRACE_PACKFILE=/Users/jason/repos/gitmask/packfile.txt GIT_TRACE_CURL=2 GIT_CURL_VERBOSE=2 git push test beta2


cd /tmp/tmp7ci900n2
git unpack-objects -r < /Users/jason/repos/gitmask/packfile.txt

```


# References

- https://janakiev.com/blog/python-shell-commands/
- https://mincong.io/2018/05/04/git-and-http/
- https://github.com/qhzhyt/http-git-server





# Goals for V2

- ability to use gitmask as a remote, rather than requiring bundles to use it.
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

- Can we use a Github App to handle fork & PR creation, rather than using a "Github Anonymous" user?
- We should show progress logs to users, showing them whats going on with the PR, and the current status/error w/ a link
- ** FUTURE ** ability for users to anonymously make comments on a PR or make follow up commits? one time API token on every push?



# Logo

[hacker icon designed by sultan mohammed](https://thenounproject.com/term/hacker/2481442)

----

# Resources



- http://weininger.net/configuration-of-nginx-for-gitweb-and-git-http-backend.html
- https://gist.github.com/massar/9399764
- https://stackoverflow.com/questions/22891148/nginx-how-to-run-a-shell-script-on-every-request
- https://github.com/markvnext/nginx-luarocks-docker/blob/master/nginx.sh
- https://git-scm.com/docs/git-http-backend
- https://apuntesderootblog.wordpress.com/2015/06/01/how-to-run-gitweb-and-git-http-backend-with-nginx-in-fedora/
- https://help.github.com/articles/changing-author-info/
- https://help.github.com/articles/pushing-to-a-remote/

# Why?

- popcornhour
- shadowproxy
- bitcoin
- truecrypt
- rapid7/metasploit-framework
- magnumripper/JohnTheRipper
- tor
- bittorrent
- http://www.eremedia.com/sourcecon/how-to-find-almost-any-github-users-email-address/
- http://www.businessinsider.com/joke-github-dicss-project-goes-nuts-2015-3
- https://github.com/letsgetrandy/brototype
- https://github.com/letsgetrandy/DICSS
- http://developers.slashdot.org/story/15/03/22/1748238/a-software-project-full-of-male-anatomy-jokes-causes-controversy

# Related projects

 * [Anonymous Github](https://github.com/tdurieux/anonymous_github) is a proxy server to support anonymous browsing of Github repositories for open-science code and data.

 * [blind-reviews](https://github.com/zombie/blind-reviews/) hides the name of a pull request submitter in the browser, to help maintainers break bias habits and take a first look at the code on its own merits. (It does not change the identifying information.)

# How to run gitmask in your serverless environment

For testing purpose, so on.

## Prerequisites

* AWS account where your gitmask run.
* Install nodejs, serverless-framework and aws-cli.
    * https://nodejs.org/
    * https://serverless.com/
    * https://aws.amazon.com/cli/

## Steps to run gitmask

1. Create and setup the AWS user for the deployment.

     * Set up the credentials with `aws configure`
     * You may use the AWS account root user.
     * You can create a new IAM user with restrict permissions.
        * https://serverless.com/blog/abcs-of-iam-permissions/ may help you.

2. Issue your github access token

    * Go to github Settings > Developer settings > Personal access tokens
    * Run generate new token
        * scopes
            * public_repo

3. Configure following environment variables:

    |Variable                 |Value  |
    |:------------------------|:-------------|
    |GITHUB_API_TOKEN         |github personal access token|
    |GITHUB_USER              |github username of the personal access token|
    |GITMASK_SERVICE          |Your own service name for gitmask, e.g. myown-gitmask-api.|
    |GITMASK_SERVICE_NORMALIZE|Normalized value for GITMASK_SERVICE,removing special characters and captalize the first letter. e.g. Myowngitmaskapi |
    |CIRCLE_SHA1              |Set the value retrieved by `git rev-parse --short HEAD`|

4. Run deployment

    ```
    sls deploy
    ```

    * The URLs for endpoints are shown.
        * You can redisplay that with `sls info`

### To remove the deployment

You can uninstall the deployment with `sls remove`.
You have to have the S3 bucket (GITMASK_SERVICE)-(stage)-upload empty in advance.
