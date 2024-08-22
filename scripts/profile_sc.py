#!/usr/bin/env python3

from siliconcompiler import Chip
import cProfile
import pstats
from pstats import SortKey
import graphviz
import argparse
import tempfile
import os
import gprof2dot


def print_stats(pr):
    ps = pstats.Stats(pr).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(20)


def generate_graph(pr, name):
    with tempfile.TemporaryDirectory() as d:
        stats = os.path.join(d, 'profile.pstats')
        dot_file = os.path.join(d, 'profile.dot')

        pr.dump_stats(stats)

        gprof2dot.main(argv=['-f', 'pstats', stats, '-o', dot_file])

        with open(dot_file) as f:
            dot = graphviz.Source(f.read())

    try:
        dot.render(filename=name, format='png', cleanup=True)
    except graphviz.ExecutableNotFound:
        pass


def run_read_manifest(pr, extra):
    remove_path = False
    if not extra:
        chip = Chip('write')
        chip.load_target('freepdk45_demo')
        chip.load_target('skywater130_demo')
        chip.load_target('asap7_demo')

        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)

        chip.write_manifest(path)
        remove_path = True
    else:
        path = extra

    chip = Chip('read')

    pr.enable()
    chip.read_manifest(path)
    pr.disable()

    if remove_path:
        os.remove(path)


def run_write_manifest_abspath(pr, extra):
    run_write_manifest(pr, extra, True)


def run_write_manifest(pr, extra, abspath=False):
    chip = Chip('write')
    chip.load_target('freepdk45_demo')
    chip.load_target('skywater130_demo')
    chip.load_target('asap7_demo')
    if extra:
        chip.load_target(extra)

    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)

    pr.enable()
    chip.write_manifest(path, abspath=abspath)
    pr.disable()


def run_asic_demo(pr, extra):
    chip = Chip('')

    pr.enable()
    chip.load_target('asic_demo')
    chip.run()
    chip.summary()
    pr.disable()


if __name__ == "__main__":
    tests = {
        'read_manifest': run_read_manifest,
        'write_manifest': run_write_manifest,
        'write_manifest_abspath': run_write_manifest_abspath,
        'asic_demo': run_asic_demo,
        'all': None
    }

    parser = argparse.ArgumentParser(
        description='Utility tool to aide in profiling SiliconCompiler')
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print the time stats from the profile')
    parser.add_argument(
        '--profile',
        choices=tests.keys(),
        default='all',
        help='Profile test to run')
    parser.add_argument(
        '--extra',
        metavar='<payload>',
        help='extra payload information for test')

    args = parser.parse_args()

    test_set = args.profile
    if test_set == 'all':
        test_set = [t for t in tests.keys() if t != 'all']
    else:
        test_set = [test_set]

    for test in test_set:
        print(f'Running {test}')
        func = tests[test]
        pr = cProfile.Profile()
        func(pr, args.extra)
        generate_graph(pr, test)
        if args.print:
            print_stats(pr)
