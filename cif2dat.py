#!/usr/bin/env python

import sys

from sasCIFtoolbox import export_toolbox
from sasCIFtoolbox import cifutils
from mmCif import mmcifIO


def main(argv):
    HELP_MESSAGE = 'cif2dat.py <sasciffile>'

    sasCIFfile = cifutils.getCifExtractOpt(argv, HELP_MESSAGE)

    sasCIFIn = mmcifIO.CifFileReader()
    sasCIFDict = sasCIFIn.read(sasCIFfile)

    sasCIFdat = export_toolbox.sasCIFsource()
    sasCIFdat.extractDat(sasCIFDict, sasCIFfile)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
