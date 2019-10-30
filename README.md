<p align="center">
  <a href="https://github.com/AnalogJ/gitmask">
  <img width="300" alt="gitmask_view" src="https://github.com/AnalogJ/gitmask/raw/beta/docs/noun_hacker_2481442.png">
  </a>
</p>

# Gitmask **Work-In-Progress**



# Goals for V2

- ability to use gitmask as a remote, rather than requiring bundles to use it.
    - https://github.com/substack/git-http-backend
    - https://github.com/asim/git-http-backend
    - https://github.com/dvdotsenko/git_http_backend.py
    - https://git-scm.com/book/no-nb/v1/Git-Internals-Transfer-Protocols
    - https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols
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
