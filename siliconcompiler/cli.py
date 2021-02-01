# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.

#Standard Modules
import sys
import logging
import argparse
import os
import re
import json
import sys
import importlib.resources

#Shorten siliconcompiler as sc
import siliconcompiler as sc
from siliconcompiler.schema import schema

###########################
def cmdline():
    '''Handles the command line configuration usign argparse. 
    All configuration parameters are exposed at the command line interface.
    This is outside of the class since this can be called 

    '''
    def_cfg = schema()

    os.environ["COLUMNS"] = '100'

    # Argument Parser
    
    parser = argparse.ArgumentParser(prog='sc',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
                                     prefix_chars='-+',
                                     description="Silicon Compiler Collection (SC)")

    # Required positional source file argument
    parser.add_argument('sc_source',
                        nargs='+',
                        help=def_cfg['sc_source']['help'])

    #Recursive argument adder
    add_arg(def_cfg, parser)
    
    #Parsing args and converting to dict
    cmdargs = vars(parser.parse_args())

    print(cmdargs)
    
    # Copying flat parse_args to nested cfg dict based on key type
    # Values are lists of varying legnth based on cfg parameter
    # stdlib, macro, tool has length 3 or 4 depending on type
    # (timing, cells, power has length 4)
    # Format is "key(s) val"

    #scalars, list, lists of lists need to be treated
    #destination is the nested cfg dictionary

    cfg= {}
    
    for key,all_vals in cmdargs.items():
       
        switch = key.split('_')       
        param = switch[0] + "_" + switch[1]
        if param not in cfg:
            cfg[param] = {}

        #Iterate over list since these are dynamic
        if switch[1] in ('stdcell', 'macro', 'tool'):
            for val in all_vals:
                if val[0] not in cfg[param]:
                        cfg[param][val[0]]={}
                if switch[2] not in cfg[param][val[0]].keys():
                        cfg[param][val[0]][switch[2]] = {}
                if switch[2] in ('timing', 'power', 'cells'):
                    if val[1] not in cfg[param][val[0]][switch[2]].keys():
                        cfg[param][val[0]][switch[2]][val[1]]={}
                        cfg[param][val[0]][switch[2]][val[1]]['value'] = val[2]
                    else:
                        cfg[param][val[0]][switch[2]][val[1]]['value'].extend(val[2])
                else:
                    if 'value' not in cfg[param][val[0]][switch[2]].keys():
                        cfg[param][val[0]][switch[2]]['value'] = val[1]
                    else:
                        cfg[param][val[0]][switch[2]]['value'].extend(val[1])
        else:
            if 'value' not in cfg:
                 cfg[param] = {}
                 cfg[param]['value'] = all_vals

            else:
                cfg[param]['value'].extend(all_vals)

    return cfg

###########################
def add_arg(cfg, parser, keys=None):
    ''' Recursively add command line arguments from cfg dictionary
    '''
    if keys is None:
        keys = []
    for k,v in sorted(cfg.items()):
        #No command line switches for these
        if k in ('sc_source', 'sc_stages'):
            pass
        #Large number of stages, so minimizing the command lines
        elif k in ('sc_tool'):
            for k2 in cfg['sc_tool']['syn'].keys():
                parser.add_argument(cfg[k]['syn'][k2]['switch'],
                                    dest=k+"_"+k2,
                                    metavar=cfg[k]['syn'][k2]['switch_args'],
                                    action='append',
                                    help=cfg[k]['syn'][k2]['help'],
                                    default = argparse.SUPPRESS)
        #All others
        else:            
            newkeys =  keys.copy()
            newkeys.append(str(k))
            if 'defvalue' in cfg[k].keys():
                keystr = '_'.join(newkeys)                
                parser.add_argument(cfg[k]['switch'],
                                    metavar=cfg[k]['switch_args'],
                                    dest=keystr,
                                    action='append',
                                    help=cfg[k]['help'],
                                    default = argparse.SUPPRESS)
            else:
                newkeys.append(str(k))
                add_arg(cfg[k], parser, keys=newkeys) 

###########################
def main():

    scriptdir = os.path.dirname(os.path.abspath(__file__))
    rootdir = re.sub("siliconcompiler/siliconcompiler", "siliconcompiler", scriptdir, 1)
    pdkcfg = rootdir + "/pdklib/virtual/nangate45/nangate45.json"
    ipcfg = rootdir + "/iplib/virtual/nangate45/NangateOpenCellLibrary.json"
    edacfg = rootdir + "/edalib/asic/sc_asicflow.json"


    #Command line inputs, read once
    cmdlinecfg = cmdline()

    #Create one (or many...) instances of Chip class
    mychip = sc.Chip()
    
    # Reading in default config files unless cfg file is set
    if 'nangate45' in cmdlinecfg['sc_target']['value']:
        mychip.readcfg(edacfg)
        mychip.readcfg(pdkcfg)
        mychip.readcfg(ipcfg)
    
    # Reading in user variables
    mychip.readenv()

    # Reading in command line arguments
    mychip.mergecfg(cmdlinecfg)
    
    #Resolve as absolute paths (should be a switch)
    mychip.abspath()

    #Creating hashes for all sourced files
    #mychip.hash()

    #Lock chip configuration
    mychip.lock()
    
    #Printing out run-config
    mychip.writecfg("sc_setup.json")

    all_stages = mychip.get('sc_stages')
    for stage in all_stages:
        mychip.run(stage)
    
    
#########################
if __name__ == "__main__":    
    sys.exit(main())
