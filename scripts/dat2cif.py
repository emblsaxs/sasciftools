#!/usr/bin/env python

import sys
import collections

from sasciftools.sasCIFtoolbox import import_toolbox, cifutils
from sasciftools.mmCif import mmcifIO


def main(argv=sys.argv[1:]):
    HELP_MESSAGE = 'dat2cif.py [-i <input_file>] [-o <output_file>] <datfile> '
    NO_FILENAME_PROVIDED_MESSAGE = 'ERROR: Please specify a .dat file'

    datfile, sasCIFfile, outputsasCIFfile = cifutils.getCifOpt(argv, HELP_MESSAGE, NO_FILENAME_PROVIDED_MESSAGE)

    if sasCIFfile:
        sasCIFIn = mmcifIO.CifFileReader()
        sasCIFDict = sasCIFIn.read(sasCIFfile)
    else:
        sasCIFDict = collections.OrderedDict()

    sasCIFdat = import_toolbox.sasdata(datfile, sasCIFDict)
    sasCIFdat.addDat(data_block_id='DAT_' + datfile[0:-4])
    sasCIFdat.addMeta(data_block_id='DAT_' + datfile[0:-4])

    sasCIFOut = mmcifIO.CifFileWriter(outputsasCIFfile)
    sasCIFOut.write(sasCIFDict)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
