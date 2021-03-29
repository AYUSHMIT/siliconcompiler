
import os
import sys
import re

####################################################
# PDK Setup
####################################################

def setup_platform(chip):

    foundry = 'virtual'
    process = 'freepdk45'
    rev = 'r1p0'
    stackup = '10M'
    edavendor = 'openroad'
    libtype = '10t'
    pdkdir = '/'.join(["asic",
                       foundry,
                       process,
                       'pdk',
                       rev])
    
    # process name
    chip.add('pdk','foundry', foundry)
    chip.add('pdk','process', process)
    chip.add('pdk','rev', rev)
    chip.add('pdk','stackup', stackup)
   
    # DRC
    chip.add('flow','drc','script',
             pdkdir+'/runsets/klayout/freepdk45.lydrc')

    # DISPLAY
    chip.add('flow','gdsview','script',
             pdkdir+'/setup/klayout/freepdk45.lyt')

    # hard coded target lib
    chip.add('asic', 'stackup', stackup)

    # APR tech file
    chip.add('pdk','aprtech',stackup, libtype, edavendor,
             pdkdir+'/apr/freepdk45.tech.lef')

    # Techlef Overrides
    chip.add('pdk','aprlayer',stackup, 'metal1 X 0.095 0.19')
    chip.add('pdk','aprlayer',stackup, 'metal1 Y 0.07  0.14')
    chip.add('pdk','aprlayer',stackup, 'metal2 X 0.095 0.19')
    chip.add('pdk','aprlayer',stackup, 'metal2 Y 0.07  0.14')
    chip.add('pdk','aprlayer',stackup, 'metal3 X 0.095 0.19')
    chip.add('pdk','aprlayer',stackup, 'metal3 Y 0.07  0.14')
    chip.add('pdk','aprlayer',stackup, 'metal4 X 0.095 0.28')
    chip.add('pdk','aprlayer',stackup, 'metal4 Y 0.07  0.28')
    chip.add('pdk','aprlayer',stackup, 'metal5 X 0.095 0.28')
    chip.add('pdk','aprlayer',stackup, 'metal5 Y 0.07  0.28')
    chip.add('pdk','aprlayer',stackup, 'metal6 X 0.095 0.28')
    chip.add('pdk','aprlayer',stackup, 'metal6 Y 0.07  0.28')
    chip.add('pdk','aprlayer',stackup, 'metal7 X 0.095 0.8')
    chip.add('pdk','aprlayer',stackup, 'metal7 Y 0.07  0.8')
    chip.add('pdk','aprlayer',stackup, 'metal8 X 0.095 0.8')
    chip.add('pdk','aprlayer',stackup, 'metal8 Y 0.07  0.8')
    chip.add('pdk','aprlayer',stackup, 'metal9 X 0.095 1.6')
    chip.add('pdk','aprlayer',stackup, 'metal9 Y 0.07  1.6')
    chip.add('pdk','aprlayer',stackup, 'metal10 X 0.095 1.6')
    chip.add('pdk','aprlayer',stackup, 'metal10 Y 0.07 1.6')
    
#########################
if __name__ == "__main__":    

    # File being executed
    prefix = os.path.splitext(os.path.basename(__file__))[0]
    output = prefix + '.json'

    # create a chip instance
    chip = siliconcompiler.Chip()
    # load configuration
    setup_pdk(chip)
    # write out result
    chip.writecfg(output)

   
