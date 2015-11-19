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


class saxsdocout(object):

    def writeProperties(self, propertiesDict, outFile):
        for prop in propertiesDict.keys():
            outFile.write(prop+': '+propertiesDict[prop]+'\n')
  
    def writeText(self, text, outFile):
        outFile.write(text)

    def writeCurves(self, curvesList, outFile, header = ''):
        # curvesList is list of lists, i.e. table
        if header:
            if len(header) == len(curvesList):
                for colIndex in range(len(header)):
                    curvesList[colIndex].insert(0, header[colIndex])
            else:
                sys.exit('writesaxsdoc: Wrong header length')

        entryLen = []
        for col in curvesList:
            entryLen.append(len(max(col, key=len)))

        for rowIndex in range(len(curvesList[0])):
            row_items = [curvesList[i][rowIndex].rjust(entryLen[i]) for i in range(len(curvesList))]
            outFile.write(" ".join(row_items) + "\n")