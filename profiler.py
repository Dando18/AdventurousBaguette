'''
Daniel Nichols
March 2021
'''
from sh import Command
import os
from util import vprint

def get_profiler(profiler_settings):
    profiler_name = profiler_settings['profiler']

    if profiler_name == 'gprof':
        return GProfProfiler(profiler_settings)
    elif profiler_name == 'hpctoolkit':
        return HPCToolkitProfiler(profiler_settings)
    else:
        print('Unknown profiler type')
        return None


class Profiler:
    def __init__(self, profiler_settings, verbose=False):
        self.profiler_settings = profiler_settings
        self.verbose = verbose


class GProfProfiler(Profiler):
    def __init__(self, profiler_settings, verbose=False):
        super().__init__(profiler_settings, verbose)


    def profile(self, repo):
        # for gprof we can run each test in the application
        # however, we must move and/or rename gman.out each time
        # and then we should go ahead and
        for test in repo.itertests():
            vprint(args.verbose, 'Profiling test \'{}\'...'.format(test['name']))
            cmd = Command(os.path.join(test['prefix'], test['executable']))

            try:
                cmd(test['args'])
            except:
                vprint(self.verbose, 'Running test \'{}\' failed...'.format(test['name']))



class HPCToolkitProfiler(Profiler):
    def __init__(self, profiler_settings, verbose=False):
        super().__init__(profiler_settings, verbose)

    def profile(self):
        pass

    