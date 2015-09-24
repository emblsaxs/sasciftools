#!/usr/bin/env python

import sys

from sasciftools.sasCIFtoolbox import export_toolbox, cifutils
from sasciftools.mmCif import mmcifIO


def main(argv=sys.argv[1:]):
    HELP_MESSAGE = 'cif2fit.py <sasciffile>'

    sasCIFfile = cifutils.getCifExtractOpt(argv, HELP_MESSAGE)

    sasCIFIn = mmcifIO.CifFileReader()
    sasCIFDict = sasCIFIn.read(sasCIFfile)

    sasCIFfit = export_toolbox.sasCIFsource()
    sasCIFfit.extractFit(sasCIFDict, sasCIFfile)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
