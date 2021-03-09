'''
Daniel Nichols
March 2021
'''
from sh import Command
import os
from util import vprint

def get_profiler(profiler_settings, verbose):
    profiler_name = profiler_settings['profiler']

    if profiler_name == 'gprof':
        return GProfProfiler(profiler_settings, verbose=verbose)
    elif profiler_name == 'hpctoolkit':
        return HPCToolkitProfiler(profiler_settings, verbose=verbose)
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
        # and then we should go ahead and read hatchet profile
        profiles = {}
        for test in repo.itertests():
            vprint(self.verbose, 'Profiling test \'{}\'...'.format(test['name']))
            exec_path = os.path.join(test['prefix'], test['executable'])
            cmd = Command(exec_path)

            try:
                cmd(test['args'])
            except:
                vprint(self.verbose, 'Running test \'{}\' failed...'.format(test['name']))
                continue

            if not os.path.isfile('gmon.out'):
                vprint(self.verbose, 'Unable to read profile...')
                continue

            # read in profile with gprof and gprof2dot
            dotfile_name = 'profile-dot-graph.dot'
            gprof = Command('gprof')
            gprof2dot = Command('gprof2dot')
            with open(dotfile_name, 'w+') as outFile:
                gprof2dot(gprof(exec_path), '-n0', '-e0', _out=outFile)

            # finally read this into hatchet
            gf = ht.GraphFrame.from_gprof_dot(dotfile_name)

            profiles[test['name']] = gf

        return profiles


class HPCToolkitProfiler(Profiler):
    def __init__(self, profiler_settings, verbose=False):
        super().__init__(profiler_settings, verbose)

    def profile(self):
        pass

    