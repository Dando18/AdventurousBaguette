'''
Daniel Nichols
March 2021
'''
from sh import git, bash, basename
from util import vprint


class Repo:
    
    def __init__(self, repo_settings, verbose=False):
        self.repo_settings = repo_settings
        self.verbose = verbose

    def clone(self):
        vprint(self.verbose, 'Cloning \'{}\'...'.format(self.repo_settings['url']))
        git.clone(self.repo_settings['url'])

    def name(self):
        return str(basename(self.repo_settings['url'], '.git')).strip()

    def get_hashes(self):
        return self.repo_settings['hashes']

    def checkout_hash(self, hash):
        vprint(self.verbose, 'Checking out hash \'{}\'...'.format(hash))
        git.checkout(hash)

    def build(self):
        vprint(self.verbose, 'Building...')
        command_runner = bash.bake('-c')
        for command in self.repo_settings['build']['commands']:
            command_runner(command)

    def remove(self):
        pass

    def itertests(self):
        for test in self.repo_settings["tests"]:
            yield test