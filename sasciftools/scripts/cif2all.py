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

import os
import sys
import getopt

from sasciftools.sasCIFtoolbox import export_toolbox
from sasciftools.mmCif import mmcifIO


def main(argv=sys.argv[1:]):
    HELP_MESSAGE = 'cif2all.py [-o <output folder>] <input file>'

    outputDir = ''

    try:
        opts, args = getopt.getopt(argv, 'ho:', ['ifile='])
    except getopt.GetoptError:
        sys.exit(HELP_MESSAGE)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit(HELP_MESSAGE)
        elif opt in ('-o', '--output'):
            outputDir = arg
    if not args and '-h' not in argv:
        sys.exit('ERROR: Please specify a .sascif file')
    else:
        sasCIFfile = args[0]

    if not os.path.isfile(sasCIFfile):    
        sys.exit('ERROR: Please specify an existing input .sascif file')

    sasCIFIn = mmcifIO.CifFileReader()
    sasCIFdict = sasCIFIn.read(sasCIFfile)

    fullOutputDir = os.path.realpath(os.path.join(os.getcwd(), outputDir))
    try:
        os.mkdir(fullOutputDir)
        os.chdir(fullOutputDir)
    except EnvironmentError:
        os.chdir(fullOutputDir)
    sasCIFinput = export_toolbox.sasCIFsource()
    sasCIFinput.extractAll(sasCIFdict, sasCIFfile)

    sys.exit(0)

if __name__ == '__main__':

    main(sys.argv[1:])
