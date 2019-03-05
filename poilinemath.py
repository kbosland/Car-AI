import math

WIDTH = 1200
HEIGHT = 600   

def rectLineIntersect (x, y, w, h, pt1, pt2):
    rectL1 = ((x,y), (x+w,y))
    rectL2 = ((x,y), (x,y+h))
    rectL3 = ((x+w,y), (x+w,y+h))
    rectL4 = ((x,y+h), (x+w,y+h))

    poi1 = calculatePOI((x,y),(x+w,y), pt1, pt2) != False
    poi2 = calculatePOI((x,y),(x,y+h), pt1, pt2) != False
    poi3 = calculatePOI((x+w,y),(x+w,y+h), pt1, pt2) != False
    poi4 = calculatePOI((x,y+h),(x+w,y+h), pt1, pt2) != False

    return poi1 or poi2 or poi3 or poi4

def getSlope (pt1, pt2):
    x1, x2, y1, y2 = pt1[0], pt2[0], pt1[1], pt2[1]
    slope = None

    if ((x2 - x1) != 0):
        slope = (y2 - y1) / (x2 - x1)

def distance (pt1, pt2):
    return int (math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2))

def pointOnLine (ptA, pt1, pt2):
    offset = 1

    x1, x2, y1, y2 = pt1[0], pt2[0], pt1[1], pt2[1]
    slopeOne = None

    if ((x2 - x1) != 0):
        slopeOne = (y2 - y1) / (x2 - x1)

    #next, calculate the y intercept of each line (b value)
    if (slopeOne != None):
        bOne = pt1[1] - (slopeOne) * pt1[0]
    else:
        bOne = pt1[0]

    if slopeOne == None:
        return abs( pt1[0] - ptA[0] ) <= offset
    elif slopeOne == 0:
        return abs( ptA[1] - bOne ) <= offset
    elif slopeIsValid(slopeOne):
        return abs( ptA[1] - ( slopeOne * ptA[0] + bOne)  ) <= offset
    
def calculatePOI (pt1, pt2, ptA, ptB):

    #first, calculate slope of each line
    x1, x2, y1, y2 = pt1[0], pt2[0], pt1[1], pt2[1]
    slopeOne = None

    if ((x2 - x1) != 0):
        slopeOne = (y2 - y1) / (x2 - x1)

    x1, x2, y1, y2 = ptA[0], ptB[0], ptA[1], ptB[1]
    #print (x1, x2)
    slopeTwo = None
    if ((x2 - x1) != 0):
        slopeTwo = (y2 - y1) / (x2 - x1)

    #next, calculate the y intercept of each line (b value)
    if (slopeOne != None):
        bOne = pt1[1] - (slopeOne) * pt1[0]
    else:
        bOne = pt1[0]

    if (slopeTwo != None):
        bTwo = ptA[1] - (slopeTwo) * ptA[0]
    else:
        bTwo = ptA[0]

    if slopeOne == slopeTwo:
        return False
    elif slopeOne == None and slopeTwo == 0:
        poi = (pt1[0], ptA[1])
    elif (slopeOne == 0 and slopeTwo == None):
        poi = (ptA[0], pt1[1])
    elif (slopeIsValid(slopeOne) and slopeTwo == None):
        poi = (ptA[0], ptA[0]*slopeOne + bOne)
    elif (slopeIsValid(slopeTwo) and slopeOne == None):
        poi = (pt1[0], pt1[0]*slopeTwo + bTwo)
    elif (slopeIsValid(slopeOne) and slopeTwo == 0):
        poi = ((bTwo - bOne) / slopeOne, bTwo)
    elif (slopeIsValid(slopeTwo) and slopeOne == 0):
        poi = ((bOne - bTwo) / slopeTwo, bOne)
    elif (slopeIsValid(slopeOne) and slopeIsValid(slopeTwo) and slopeTwo < 0) :
        poi = ((bTwo - bOne) / (slopeOne - slopeTwo), slopeOne * ((bTwo - bOne) / (slopeOne - slopeTwo)) + bOne)
    elif (slopeIsValid(slopeOne) and slopeIsValid(slopeTwo) and slopeTwo > 0) :
        poi = ((bOne - bTwo) / (slopeTwo - slopeOne), slopeTwo * ((bOne - bTwo) / (slopeTwo - slopeOne)) + bTwo)

    if (poiIsValid(poi, pt1, pt2, ptA, ptB)):
        return (int(poi[0]), int(poi[1]))
    else:
        return False

def slopeIsValid (number):
    return number != 0 and number != None

def isBetween (poi, pt1, pt2, ptA, ptB):

    #Checking if POI is in the sensor range
    minX =  min([item[0] for item in [pt1, pt2]])
    minY =  min([item[1] for item in [pt1, pt2]])
    maxX =  max([item[0] for item in [pt1, pt2]])
    maxY =  max([item[1] for item in [pt1, pt2]])
    inSensorRange = poi[0] >= minX and poi[0] <= maxX and poi[1] >= minY and poi[1] <= maxY

    #Checking if POI is in the line's range
    minX =  min([item[0] for item in [ptA, ptB]])
    minY =  min([item[1] for item in [ptA, ptB]])
    maxX =  max([item[0] for item in [ptA, ptB]])
    maxY =  max([item[1] for item in [ptA, ptB]])
    inLinesRange = poi[0] >= minX and poi[0] <= maxX and poi[1] >= minY and poi[1] <= maxY

    return inSensorRange and inLinesRange

def poiIsValid (poi, pt1, pt2, ptA, ptB):
    if (poi[0] >= 0 and poi[0] <= WIDTH and poi[1] >= 0 and poi[1] <= HEIGHT):
        if (pointOnLine(poi, pt1, pt2)):
            if (isBetween(poi, pt1, pt2, ptA, ptB)):
                return True

    return False

def angleOfIntersection (pt1, pt2, ptA, ptB):
    #first, calculate slope of each line
    x1, x2, y1, y2 = pt1[0], pt2[0], pt1[1], pt2[1]
    slopeOne = None

    if ((x2 - x1) != 0):
        slopeOne = (y2 - y1) / (x2 - x1)

    x1, x2, y1, y2 = ptA[0], ptB[0], ptA[1], ptB[1]
    slopeTwo = None
    if ((x2 - x1) != 0):
        slopeTwo = (y2 - y1) / (x2 - x1)

    if (slopeOne == slopeTwo):
        return False
    elif (slopeOne == None and slopeTwo == 0):
        return 90
    elif (slopeTwo == None and slopeOne == 0):
        return 90
    elif (slopeIsValid(slopeOne) and slopeTwo == None):
        return abs( 180 - abs(int(0 - math.degrees((math.atan(slopeOne))))))
    elif (slopeIsValid(slopeTwo) and slopeOne == None):
        return abs( 180 - abs(int(0 - math.degrees((math.atan(slopeTwo))))))
    else:
        return abs(180 - int (abs(int((math.degrees((math.atan(slopeOne))) - math.degrees((math.atan(slopeTwo))) )))))