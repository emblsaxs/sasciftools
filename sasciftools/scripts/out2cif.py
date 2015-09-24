#!/usr/bin/env python

import sys
import collections

from sasciftools.sasCIFtoolbox import import_toolbox, cifutils
from sasciftools.mmCif import mmcifIO


def main(argv=sys.argv[1:]):
    HELP_MESSAGE = 'out2cif.py [-i <input_file>] [-o <output_file>] <outfile>'
    NO_FILENAME_PROVIDED_MESSAGE = 'ERROR: Please specify a .out file'

    outfile, sasCIFfile, outputsasCIFfile = cifutils.getCifOpt(argv, HELP_MESSAGE, NO_FILENAME_PROVIDED_MESSAGE)

    if sasCIFfile:
        sasCIFIn = mmcifIO.CifFileReader()
        sasCIFDict = sasCIFIn.read(sasCIFfile)
    else:
        sasCIFDict = collections.OrderedDict()

    sasCIFpR = import_toolbox.sasdata(outfile, sasCIFDict)
    sasCIFpR.addOut(data_block_id="OUT_" + outfile[0:-4])

    sasCIFOut = mmcifIO.CifFileWriter(outputsasCIFfile)
    sasCIFOut.write(sasCIFDict)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
