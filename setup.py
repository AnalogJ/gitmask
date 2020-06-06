from setuptools import setup, find_namespace_packages


setup(
    name='gitmask',

    version='1',

    description='',
    long_description='',

    author='Jason Kulatunga',
    author_email='jason@thesparktree.com',

    license='MIT',

    packages=find_namespace_packages(include=['gitmask.*', 'gitmask.lib.*']),
    zip_safe=False,
)
