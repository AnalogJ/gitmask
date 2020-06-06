from dulwich.server import Backend
from dulwich import log_utils
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo
from github import Github

# from github_repo import GithubRepo

import os
from gitmask.lib.scm.github_repo import GithubRepo

logger = log_utils.getLogger(__name__)

class GithubBackend(Backend):
    """Backend looking up Git repositories from scm"""

    def __init__(self):
        super(GithubBackend, self).__init__()
        # or using an access token
        self.scm_client = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))


    def open_repository(self, repo_fullname):
        logger.debug('opening github repository at %s', repo_fullname)

        try:
            # check if repo exists
            repo = self.scm_client.get_repo(repo_fullname)
            return GithubRepo(repo_fullname)
        except:
            raise NotGitRepository("Github Repository %r does not exist" % (repo_fullname))

# if __name__ == "__main__":
#     backend = GithubBackend()
#     repo = backend.open_repository("AnalogJ/gitmask")
#     print(sorted(repo.get_refs().items()))
#     print(sorted(repo.refs.get_symrefs().items()))
