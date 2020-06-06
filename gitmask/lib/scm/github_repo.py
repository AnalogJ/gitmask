from dulwich.repo import BaseRepo
from dulwich.object_store import MemoryObjectStore
from gitmask.lib.scm.github_refs_container import GithubRefsContainer
import os
from github import Github

# Based on BaseRepo(object): https://github.com/dulwich/dulwich/blob/master/dulwich/repo.py#L273
# and MemoryRepo(BaseRepo): https://github.com/dulwich/dulwich/blob/master/dulwich/repo.py#L1384
# and Repo(BaseRepo): https://github.com/dulwich/dulwich/blob/master/dulwich/repo.py#L912
class GithubRepo(BaseRepo):
    """A git repository backed by local disk.
    To open an existing repository, call the contructor with
    the path of the repository.
    To create a new repository, use the Repo.init class method.
    """

    def __init__(self, repo_fullname):
        self.scm_client = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
        self.repo_fullname = repo_fullname
        self.scm_client.get_repo(self.repo_fullname) # throws error if repo does not exist.


        self._reflog = []
        refs_container = GithubRefsContainer(self.repo_fullname)
        BaseRepo.__init__(self, MemoryObjectStore(), refs_container)
        self._named_files = {}
        self.bare = True
        self._config = None
        self._description = None

# if __name__ == "__main__":
#     repo = GithubRepo("AnalogJ/gitmask")
#     print(sorted(repo.get_refs().items()))
#     print(sorted(repo.refs.get_symrefs().items()))
