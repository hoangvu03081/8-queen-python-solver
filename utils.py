import sys
import re

def void():
    return

def load(filepath):
    try:
        with open(filepath, 'r') as f:
            queenNum = int(f.readline())
            coordinate = f.readline()

            binaryBoard = convertCoordinateToBinary(coordinate, queenNum)
            if isinstance(binaryBoard, dict):
                return (binaryBoard, queenNum)
            return False
    except Exception as err:
        print(err)

def convertCoordinateToBinary(coordinate, n):
    if n == 0:
        queenDict = {}
        for i in range(1,65):
            queenDict[i] = False
        return queenDict
    if not re.match("(\(\d, \d\))( \(\d, \d\)){"+str(n-1)+"}", coordinate):
        return print("Error: Second line format is not correct, please check again")

    coordinateAsList = [int(num) for num in re.findall(r'\d+', coordinate)]
    toBeCheckCoordinateList = [coordinateAsList[i:i + 2] for i in range(0, len(coordinateAsList), 2)]
    if not checkValidCoordinate(toBeCheckCoordinateList):
        return print("Error: There are invalid placements of queen: attacking queens")

    queenDict = {}
    for i in range(1,65):
        queenDict[i] = False
    for queenCoord in toBeCheckCoordinateList:
        queenDict[queenCoord[0]*8 +queenCoord[1]+1] = True
    return queenDict

    i = 0
    while i < n*2:
        if coordinateAsList[i] < 1 or coordinateAsList[i] > 8 or coordinateAsList[i+1] < 1 or coordinateAsList[i+1] > 8:
            return print("Error: Some coordination is out of range [1,8]")
        queenPosition.append(coordinateAsList[i]*8 + coordinateAsList[i+1])
        i+=2
    
    temp = list("0"*64)
    for pos in queenPosition:
        temp[pos] = "1"
    return temp

def checkValidCoordinate(arr):
    for coord1 in arr:
        for coord2 in arr:
            if coord1 == coord2:
                break
            if coord1[0] == coord2[0] or coord1[1] == coord2[1] or abs(coord1[0] - coord2[0]) == abs(coord1[1] - coord2[1]):
                return False
    return True