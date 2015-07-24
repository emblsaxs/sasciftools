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