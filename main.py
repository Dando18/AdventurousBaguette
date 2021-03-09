'''
Daniel Nichols
March 2021
'''
import argparse
import hatchet
import sh
from argparse import ArgumentParser
import os
import json

from tester import Tester
from util import vprint


def read_input(json_fpath):
    obj = None
    with open(json_fpath) as f:
        obj = json.load(f)
    return obj


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='json file to read input settings')
    parser.add_argument('--working-directory', type=str, default='scratch', help='where to store files')
    parser.add_argument('-p', '--preserve', action='store_true', help='don\'t remove scratch files')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()

    input_settings = read_input(args.input)

    # move into working directory
    vprint(args.verbose, 'Creating working directory...')
    sh.mkdir('-p', args.working_directory)
    sh.cd(args.working_directory)

    # do the profiling for every application
    for application in input_settings:
        vprint(args.verbose, 'Initializing tests for \'{}\'...'.format(application['repo']['url']))
        tester = Tester(application["repo"], verbose=args.verbose)
        setup_successful = tester.setup()

        if setup_successful:
            tester.profile(application["profile"])
            tester.print_summary()
        else:
            vprint(args.verbose, 'Failed to setup \'{}\'. Skipping tests...'.format(application['repo']['url']))


    # step back and remove working directory
    vprint(args.verbose, 'Cleaning up...')
    sh.cd('..')
    if not args.preserve:
        sh.rm('-rf', args.working_directory)



if __name__ == '__main__':
    main()