#!/usr/bin/env python

# Copyright (C) 2014-2015 European Molecular Biology Laboratory (EMBL)
#
# EMBL licenses this file to you under the Apache License,
# Version 2.0 ("the License"); you may not use this file
# except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import sys

from sasciftools.sasCIFtoolbox import export_toolbox, cifutils
from sasciftools.mmCif import mmcifIO


def main(argv=sys.argv[1:]):
    HELP_MESSAGE = 'cif2pdb.py <sasciffile>'

    sasCIFfile = cifutils.getCifExtractOpt(argv, HELP_MESSAGE)

    sasCIFIn = mmcifIO.CifFileReader()
    sasCIFDict = sasCIFIn.read(sasCIFfile)

    sasCIFpdb = export_toolbox.sasCIFsource()
    sasCIFpdb.extractAtoms(sasCIFDict, sasCIFfile)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
