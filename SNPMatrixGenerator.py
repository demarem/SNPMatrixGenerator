'''
Created on Aug 28, 2013
@author: Matthew Demarest
'''

import random
from nexus import NexusReader
from nexus import NexusWriter

NUCLEOTIDES = {'A', 'T', 'G', 'C', 'a', 't', 'g', 'c'}


def snpMatrixGenerator(sourceFile, destFile, recordAll=False,
                       recordRandomSample=True):
    if recordAll == recordRandomSample:
        print "Invalid Options"
        exit()

    destNexus = NexusWriter()

    block = ""
    snpCol = 0
    for line in sourceFile:
        if all(x in line.lower() for x in {"begin", "data"}):
            sourceNexus = NexusReader()
            sourceNexus.read_string(block)
            if "data" in sourceNexus.blocks:
                snpCol = _findDifferences(sourceNexus, destNexus, snpCol,
                               recordAll, recordRandomSample)
            block = line
        else:
            block += line

    sourceNexus = NexusReader()
    sourceNexus.read_string(block)
    if "data" in sourceNexus.blocks:
        snpCol = _findDifferences(sourceNexus, destNexus, snpCol,
                       recordAll, recordRandomSample)

    destFile.write(destNexus.make_nexus() + '\n')

    destFile.close()
    sourceFile.close()


def _findDifferences(sourceNexus, destNexus, destCol,
                    recordAll=False, recordRandomSample=True):
    differentCols = []
    for i in range(len(sourceNexus.data.characters)):
        s = set(sourceNexus.data.characters[i].values())
        s = s.intersection(NUCLEOTIDES)
        if len(s) > 1:
            if recordAll:
                _addCol(sourceNexus, destNexus, i, destCol)
                destCol += 1
            elif recordRandomSample:
                differentCols.append(i)
    if recordRandomSample:
        if differentCols:
            _addCol(sourceNexus, destNexus, random.choice(differentCols),
                    destCol)
            destCol += 1

    return destCol


def _addCol(sourceNexus, destNexus, sourceCol, destCol):
    for taxa, char in sourceNexus.data.characters[sourceCol].items():
        destNexus.add(taxa, destCol, char)


if __name__ == '__main__':
    snpMatrixGenerator(open("../Example/Nexus_Ex.nex"),
            open("output.nex", "w"), recordAll=True, recordRandomSample=False)
