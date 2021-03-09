'''
Daniel Nichols
March 2021
'''
from sh import Command, rm
import hatchet as ht
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

        self.hpcrun_cmd = Command('hpcrun')
        self.hpcrun_cmd = self.hpcrun_cmd.bake('-e', 'WALLCLOCK@5000')
        self.hpcstruct_cmd = Command('hpcstruct')
        self.hpcprof_cmd = Command('mpirun')
        self.hpcprof_cmd = self.hpcprof_cmd.bake('-np', '1', 'hpcprof-mpi',  '--metric-db', 'yes')

    def profile(self, repo):
        profiles = {}
        for test in repo.itertests():
            vprint(self.verbose, 'Profiling test \'{}\'...'.format(test['name']))
            exec_path = os.path.join(test['prefix'], test['executable'])

            hpcstruct_name = '{}.hpcstruct'.format(test['name'])
            hpcmeasurements_name = 'hpctoolkit-{}-measurements'.format(test['name'])
            hpcdatabase_name = 'hpctoolkit-{}-database'.format(test['name'])

            # try to generate hpcstruct
            try:
                self.hpcstruct_cmd(exec_path, '--output', hpcstruct_name)
            except:
                vprint(self.verbose, 'Failed to create hpcstruct file...')
                continue

            # run test
            try:
                self.hpcrun_cmd('--output', hpcmeasurements_name, exec_path, test['args'])
            except:
                vprint(self.verbose, 'Running test \'{}\' failed...'.format(test['name']))
                continue

            # generate profile
            try:
                self.hpcrun_cmd('--output', hpcmeasurements_name, exec_path, test['args'])
                self.hpcprof_cmd('-S', hpcstruct_name, '-I', './+', '--output', hpcdatabase_name, hpcmeasurements_name)
            except:
                vprint(self.verbose, 'Running test \'{}\' failed...'.format(test['name']))
                continue

            # finally read hatchet profile
            profiles[test['name']] = ht.GraphFrame.from_hpctoolkit(hpcdatabase_name)

            # and now delete the leftover files/folders
            rm('-r', hpcstruct_name, hpcmeasurements_name, hpcdatabase_name)

        return profiles
            

    