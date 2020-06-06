
def auth_remote_url(authToken, org, repo):
    return "https://{0}:@github.com/{1}/{2}.git".format(authToken, org, repo)

