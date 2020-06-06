from dulwich.refs import DictRefsContainer
from github import Github
import os



# based on RefsContainer(object): https://github.com/dulwich/dulwich/blob/master/dulwich/refs.py#L95
# and DictRefsContainer(RefsContainer): https://github.com/dulwich/dulwich/blob/master/dulwich/refs.py#L390
class GithubRefsContainer(DictRefsContainer):
    """A container for refs."""

    def __init__(self, repo_fullname, logger=None):
        self.scm_client = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
        self.repo_fullname = repo_fullname
        repo = self.scm_client.get_repo(self.repo_fullname)

        # from https://github.com/dulwich/dulwich/blob/master/dulwich/tests/test_refs.py#L331
        # dict(_TEST_REFS)
        # Dict of refs that we expect all RefsContainerTests subclasses to define.
        # _TEST_REFS = {
        #    b'HEAD': b'42d06bd4b77fed026b154d16493e5deab78f02ec',
        #    b'refs/heads/40-char-ref-aaaaaaaaaaaaaaaaaa':
        #        b'42d06bd4b77fed026b154d16493e5deab78f02ec',
        #    b'refs/heads/master': b'42d06bd4b77fed026b154d16493e5deab78f02ec',
        #    b'refs/heads/packed': b'42d06bd4b77fed026b154d16493e5deab78f02ec',
        #    b'refs/tags/refs-0.1': b'df6800012397fb85c56e7418dd4eb9405dee075c',
        #    b'refs/tags/refs-0.2': b'3ec9c43c84ff242e3ef4a9fc5bc111fd780a76a8',
        #    b'refs/heads/loop': b'ref: refs/heads/loop',
        # }

        refs = {}
        for ghRefs in repo.get_git_refs():
            refs[bytes(ghRefs.ref, 'utf-8')] = bytes(ghRefs.object.sha, 'utf-8')
            # TODO: check the repo base branch
            if ghRefs.ref == 'refs/heads/master':
                refs[bytes('HEAD', 'utf-8')] = bytes(ghRefs.object.sha, 'utf-8')

        super(GithubRefsContainer, self).__init__(dict(refs), logger=logger)



if __name__ == "__main__":
    container = GithubRefsContainer("AnalogJ/gitmask")
    print(container.get_symrefs())
    # print(container.allkeys())
    # print(container._refs)
