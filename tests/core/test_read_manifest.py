# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
import os
import siliconcompiler
import copy
import json
from siliconcompiler import _metadata

import pytest

def test_read_manifest_fields():
    '''Ensure that changes to fields other than 'value' are reflected by read_manifest()'''

    chip = siliconcompiler.Chip('foo')
    chip.set('input', 'rtl', 'verilog', False, field='copy')
    chip.input('foo.v')
    chip.write_manifest('tmp.json')

    # fresh chip, so we don't retain anything from `chip` in-memory
    chip2 = siliconcompiler.Chip('foo')
    chip2.read_manifest('tmp.json')
    assert chip2.get('input', 'rtl', 'verilog', field='copy') is False


def test_read_sup():
    '''Test compressed read/write'''

    chip = siliconcompiler.Chip('foo')
    chip.input('foo.v')
    chip.write_manifest('tmp.sup.gz')

    chip2 = siliconcompiler.Chip('foo')
    chip2.read_manifest('tmp.sup.gz')
    assert chip2.get('input', 'rtl', 'verilog') == ['foo.v']

def test_modified_schema(datadir):
    '''Make sure schema has not been modified without updating defaults.json'''

    # gets default from schema
    chip = siliconcompiler.Chip('test')

    # expected
    with open(os.path.join(datadir, 'defaults.json'), 'r') as f:
        expected = json.load(f)

    # special case (initialized in constructor)
    expected['design']['value'] = 'test'
    expected['design']['set'] = True

    assert chip.schema.cfg == expected

def test_read_history():
    '''Make sure that history gets included in manifest read.'''
    chip = siliconcompiler.Chip('foo')
    chip.input('foo.v')
    chip.schema.record_history()
    chip.write_manifest('tmp.json')

    chip2 = siliconcompiler.Chip('foo')
    chip2.read_manifest('tmp.json')
    assert chip.get('input', 'rtl', 'verilog', job='job0') == ['foo.v']

def test_read_job():
    '''Make sure that we can read a manifest into a non-default job'''
    chip = siliconcompiler.Chip('foo')
    chip.input('foo.v')
    chip.write_manifest('tmp.json')

    chip2 = siliconcompiler.Chip('foo')
    chip2.read_manifest('tmp.json', job='job1')
    assert chip2.get('input', 'rtl', 'verilog', job='job1') == ['foo.v']

#########################
if __name__ == "__main__":
    from tests.fixtures import datadir
    test_modified_schema(datadir(__file__))
    test_read_sup()
