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


def getSaxsDocLibPath():
    import sys
    import os
    
    SAXSDOCLIBPATH = ''
    
    # Check if file with path exists
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    sascifiniLocation = os.path.join(__location__, 'sasciftools.ini')

    if os.path.isfile(sascifiniLocation):
        with open(sascifiniLocation) as f:
            for line in f:
                if line.startswith('SAXSDOCLIBPATH'):
                    SAXSDOCLIBPATH = line.split('=')[-1].strip()
        f.close()
    if not SAXSDOCLIBPATH or not os.path.isfile(os.path.join(SAXSDOCLIBPATH, 'saxsdocument.so')):
        SAXSDOCLIBPATH = '/usr/lib/x86_64-linux-gnu/atsas/python2.7/dist-packages/'
    if os.path.isfile(os.path.join(SAXSDOCLIBPATH, 'saxsdocument.so')):    
        sys.path.append(SAXSDOCLIBPATH)
    else: 
        exit('saxsdocument library not found. Please check SAXSDOCLIBPATH in sasciftools.ini')


def getCifOpt(argv, HELP_MESSAGE, NO_FILENAME_PROVIDED_MESSAGE):
    import getopt
    import sys
    import os

    sasCIFfile = ''
    outputsasCIFfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        sys.exit(HELP_MESSAGE)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit(HELP_MESSAGE)
        elif opt in ("-i", "--ifile"):
            sasCIFfile = arg
            if not os.path.isfile(sasCIFfile):    
                sys.exit('ERROR: Please specify an existing input .sascif file')
        elif opt in ("-o", "--ofile"):
            outputsasCIFfile = arg
    if not args and '-h' not in argv:
        sys.exit(NO_FILENAME_PROVIDED_MESSAGE)
    else:
        dataFilename = args[0]
    if not sasCIFfile and not outputsasCIFfile:
        sasCIFfile = dataFilename[0:-4] + '.sascif'
        open(sasCIFfile, 'w').close()
    if not outputsasCIFfile:
        outputsasCIFfile = sasCIFfile
    if not os.path.isfile(dataFilename):    
        sys.exit('ERROR: Please specify an existing data file')
    return dataFilename, sasCIFfile, outputsasCIFfile


def getCifExtractOpt(argv, HELP_MESSAGE):
    import getopt
    import sys
    import os

    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        sys.exit(HELP_MESSAGE)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit(HELP_MESSAGE)
    if not args and '-h' not in argv:
        sys.exit('ERROR: Please specify a .sascif file')
    else:
        sascifFilename = args[0]
    if not os.path.isfile(sascifFilename):    
        sys.exit('ERROR: Please specify an existing input .sascif file')
    return sascifFilename