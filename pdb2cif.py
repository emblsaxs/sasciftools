#!/usr/bin/env python

import sys
import collections

from sasCIFtoolbox import import_toolbox
from sasCIFtoolbox import cifutils
from mmCif import mmcifIO


def main(argv):
    HELP_MESSAGE = 'pdb2cif.py [-i <input_file>] [-o <output_file>] <pdbfile>'
    NO_FILENAME_PROVIDED_MESSAGE = 'ERROR: Please specify a .pdb file'

    pdbfile, sasCIFfile, outputsasCIFfile = cifutils.getCifOpt(argv, HELP_MESSAGE, NO_FILENAME_PROVIDED_MESSAGE)

    if sasCIFfile:
        sasCIFIn = mmcifIO.CifFileReader()
        sasCIFDict = sasCIFIn.read(sasCIFfile)
    else:
        sasCIFDict = collections.OrderedDict()

    if not outputsasCIFfile:
        outputsasCIFfile = sasCIFfile

    sasCIFpdb = import_toolbox.pdbdata(pdbfile, sasCIFDict)
    sasCIFpdb.addAtoms(data_block_id="MODEL_" + pdbfile[0:-4])

    sasCIFOut = mmcifIO.CifFileWriter(outputsasCIFfile)
    sasCIFOut.write(sasCIFDict)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
