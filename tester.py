'''
Daniel Nichols
March 2021
'''
import sh
from repo import Repo
from profiler import get_profiler
from util import vprint
from hatchet_util import find_slowest_functions, get_total_runtime


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


    def print_summary(self):
        summary_stats = {}

        print('{}:'.format(self.repo.name()))
        for git_hash, profile in self.profiles_by_hash.items():
            print('\tcommit \'{}\':'.format(git_hash))
            for test, gf in profile.items():
                print('\t\ttest \'{}\':'.format(test))

                if test not in summary_stats:
                    summary_stats[test] = {'count': 0, 'total runtime': 0}

                summary_stats[test]['count'] += 1
                
                total_runtime = get_total_runtime(gf)
                print('\t\t\ttotal runtime: {}'.format(total_runtime))
                summary_stats[test]['total runtime'] += total_runtime

                slowest_funcs = find_slowest_functions(gf, n_slowest=5)
                print('\t\t\tslowest funcs: {}'.format(slowest_funcs))
    
        print('\tSummary:')
        for test, stats in summary_stats.items():
            print('\t\ttest \'{}\':'.format(test))
            print('\t\t\taverage runtime: {}'.format(stats['total runtime'] / stats['count']))

                