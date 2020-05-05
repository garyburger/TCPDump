import re

f = open('sampletcpdump.txt', 'r')

numReads = 0
idList = []
ipDict = {}
startDict = {}
endDict = {}
ttlDict = {}
entireFile = ''
ip: str = ''
prevLine = ''
prevIp = ''
endTime = ''
ttlPrinted = False

"""
THIS HELPER FUNCTION IS NOT MY OWN
CREDIT FOR THIS HELPER FUNCTION GOES TO:
https://thispointer.com/python-how-to-find-keys-by-value-in-dictionary/
"""
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys

#READ THE FILES AND WRITE INTO THE DICTIONARIES
with open('sampletcpdump.txt', 'r') as file:
    for line in file:
        asd = str(line)
        idNum = str(re.findall("id .....", asd)).strip("['id, of']")
        ip = str(re.findall(" .............. >", asd)).strip("['    >']")
        time = str(re.findall("^1................ ", asd)).strip("[' ']")
        ttl = str(re.findall("ttl...", asd)).strip("['ttl ,']")
        #print(ttl)
        if idNum in idList:
            ipDict[idNum] = prevIp
            if startDict.get(idNum) != '':
                endDict[idNum] = endTime
        elif idNum not in idList:
            startDict[idNum] = time
            idList.append(idNum)
            ttlDict[idNum] = ttl
        prevLine = line
        prevIp = ip
        if time != '':
            endTime = time

    #CREATE A NEW FILE AND WRITE RESULTS INTO FILE
    prevTTL = ''
    outputFile = open("output.txt", "w+")
    for each in idList:
        if ttlDict[each] == prevTTL and each != '':
            continue
        elif each != '':
            try:
                printList = getKeysByValue(ipDict, ipDict[each])
                numCounts = 0
                for ids in printList:
                    if ids == '' or numCounts == 15:
                        break
                    numCounts += 1
                    if not ttlPrinted:
                        outputFile.write('TTL = ' + ttlDict[ids] + "\n")
                        outputFile.write(ipDict[ids] + "\n")
                        ttlPrinted = True
                    resultTime = float(endDict[ids])*1000 - float(startDict[ids])*1000
                    outputFile.write('Time ' + str(numCounts) + ' = ' + "{0:.3f}".format(resultTime) + " ms\n")
                ttlPrinted = False
                outputFile.write("\n")
                prevTTL = ttlDict[each]
            except KeyError:
                continue

    print("output.txt created!")
