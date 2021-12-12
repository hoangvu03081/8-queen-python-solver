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
            return (binaryBoard, queenNum)
    except Exception as err:
        print(err)

def convertCoordinateToBinary(coordinate, n):
    if n == 0:
        return list("0"*64)
    if not re.match("(\(\d, \d\))( \(\d, \d\)){"+str(n-1)+"}", coordinate):
        raise Exception("Second line format is not correct, please check again")

    coordinateAsList = [int(num) for num in re.findall(r'\d+', coordinate)]
    queenPosition = []

    i = 0
    while i < n*2:
        if coordinateAsList[i] < 0 or coordinateAsList[i] > 7 or coordinateAsList[i+1] < 0 or coordinateAsList[i+1] > 7:
            raise Exception("Some coordination is out of range [0,7]")
        queenPosition.append(coordinateAsList[i]*8 + coordinateAsList[i+1])
        i+=2
    
    temp = list("0"*64)
    for pos in queenPosition:
        temp[pos] = "1"
    return temp