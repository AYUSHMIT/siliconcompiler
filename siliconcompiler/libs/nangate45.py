import os
import copy
import siliconcompiler

def make_docs():
    '''
    Nangate open standard cell library for FreePDK45.
    '''

    chip = siliconcompiler.Chip()
    setup(chip)
    return chip

def setup(chip):

    lib = siliconcompiler.Chip()

    libname = 'nangate45'
    foundry = 'virtual'
    process = 'freepdk45'
    stackup = '10M'
    libtype = '10t'
    version = 'r1p0'
    corner = 'typical'
    objectives = ['setup']

    libdir = os.path.join('..',
                          'third_party',
                          'pdks',
                          foundry,
                          process,
                          'libs',
                          libname,
                          version)

    # name
    lib.set('design', libname)

    # version
    lib.set('package', 'version', version)

    # timing
    lib.add('model', 'timing', 'nldm-lib', corner,
             libdir+'/lib/NangateOpenCellLibrary_typical.lib')

    # lef
    lib.add('model', 'layout', 'lef', stackup,
             libdir+'/lef/NangateOpenCellLibrary.macro.mod.lef')

    # gds
    lib.add('model', 'layout', 'gds', stackup,
             libdir+'/gds/NangateOpenCellLibrary.gds')

    # site name
    lib.set('asic', 'site',
            'FreePDK45_38x28_10R_NP_162NW_34O',
            'symmetry',
            'Y')

    lib.set('asic', 'site',
            'FreePDK45_38x28_10R_NP_162NW_34O',
            'size',
            (0.19,1.4))

    # driver
    lib.add('asic', 'cells','driver', "BUF_X4")

    # clock buffers
    lib.add('asic', 'cells','clkbuf', "BUF_X4")

    # tie cells
    lib.add('asic', 'cells','tie', ["LOGIC1_X1/Z",
                                    "LOGIC0_X1/Z"])

    # buffer cell
    lib.add('asic', 'cells', 'buf', ['BUF_X1/A/Z'])

    # hold cells
    lib.add('asic', 'cells', 'hold', "BUF_X1")

    # filler
    lib.add('asic', 'cells', 'filler', ["FILLCELL_X1",
                                        "FILLCELL_X2",
                                        "FILLCELL_X4",
                                        "FILLCELL_X8",
                                        "FILLCELL_X16",
                                        "FILLCELL_X32"])

    # Stupid small cells
    lib.add('asic', 'cells', 'ignore', ["AOI211_X1",
                                        "OAI211_X1"])

    # Tapcell
    lib.add('asic', 'cells','tap', "FILLCELL_X1")

    # Endcap
    lib.add('asic', 'cells','endcap', "FILLCELL_X1")

    # Techmap
    lib.add('asic', 'file', 'yosys', 'techmap',
            libdir + '/techmap/yosys/cells_latch.v')

    lib.set('asic', 'pgmetal', 'm1')

    # TODO: this needs to be cleaned up
    chip.cfg['library'][libname] = copy.deepcopy(lib.cfg)

#########################
if __name__ == "__main__":

    lib = make_docs()
    lib.write_manifest('nangate45.tcl')
