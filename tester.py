'''
Daniel Nichols
March 2021
'''
import sh
from repo import Repo
from profiler import get_profiler
from util import vprint


def linear_iterator(items):
    for item in items:
        yield item


def get_hash_iterator(traversal_type='linear'):
    if traversal_type == 'linear':
        return linear_iterator
    elif traversal_type == 'random':
        return linear_iterator
    else:
        return linear_iterator


class Tester:
    
    def __init__(self, repo_settings, verbose=False):
        self.verbose = verbose
        self.repo_settings = repo_settings
        self.repo = Repo(self.repo_settings, verbose=self.verbose)

    def fetch(self):
        self.repo.clone()

    def build(self):
        self.repo.build()

    def setup(self):
        try:
            self.fetch()
        except:
            return False
        return True

    def profile(self, profile_settings):
        # cd into repo
        sh.cd(self.repo.name())

        # create the initial profiler
        profiler = get_profiler(profile_settings, self.verbose)

        # determine how to traverse hashes
        iter = get_hash_iterator(traversal_type=profile_settings['traversal'])

        # do the traversal
        self.profiles_by_hash = {}
        for git_hash in iter(self.repo.get_hashes()):
            # first checkout this version of the code
            self.repo.checkout_hash(git_hash)

            # then build
            try:
                self.build()
            except:
                vprint(self.verbose, 'Failed to build for hash \'{}\''.format(git_hash))

            # now do the profiling
            prof = profiler.profile(self.repo)
            self.profiles_by_hash[git_hash] = prof

        # step back out of repo
        sh.cd('..')