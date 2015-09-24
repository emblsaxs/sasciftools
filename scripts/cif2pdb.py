#!/usr/bin/env python

import sys

from sasCIFtoolbox import export_toolbox
from sasCIFtoolbox import cifutils
from mmCif import mmcifIO


def main(argv):
    HELP_MESSAGE = 'cif2pdb.py <sasciffile>'

    sasCIFfile = cifutils.getCifExtractOpt(argv, HELP_MESSAGE)

    sasCIFIn = mmcifIO.CifFileReader()
    sasCIFDict = sasCIFIn.read(sasCIFfile)

    sasCIFpdb = export_toolbox.sasCIFsource()
    sasCIFpdb.extractAtoms(sasCIFDict, sasCIFfile)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
