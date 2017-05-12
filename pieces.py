import cv2
import numpy as np;
import math
# read the image throught an window frame 
#imports for that
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
from sideOfPieces import sideOfPieces

class pieces:
    
    # init for the class pieces
    def __init__(self, image = None):
        self.image = image
        self.corners = []
        self.side = []
        self.center = []
        self.isCornerPiece = False
        self.isBorderPiece = False
        self.isCenterPiece = False

        self.pointA = []
        self.pointB = []
        self.pointC = []
        self.pointD = []
        self.name = ""
        self.listOfPoints = []
        self.testing = True


    def unittestingfunction(self):
        pointa = [9,2]
        pointb = [1,2]
        print("Liner Equation method called ---------")
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.LinerEquation(pointa,pointb))
        print("Expected Result =",[0.0,2.0])
        pointa = [1,4]
        pointb = [1,10]
        print("Liner Equation method called ---------")
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.LinerEquation(pointa,pointb))
        print("Expected Result = unexpected")

        pointa = [2,5]
        pointb = [3,8]
        print("Liner Equation method called ---------")
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.LinerEquation(pointa,pointb))
        print("Expected Result =",[3.0,-1])

        print("Number of point in between testing---------------")
        print("Test 1")
        points = [[[1,2]],[[3,4]],[[6,8]],[[5,8]],[[7,8]],[[9,10]],[[11,12]]]
        pointa = [2,5]
        pointb = [3,8]
        print("points =",points)
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.NumberOfPointInBetween(pointa,pointb,points))
        print("Expected Result = unexpected")

        print("Test 2")
        pointa = [1,2]
        pointb = [11,12]
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.NumberOfPointInBetween(pointa,pointb,points))
        print("Expected Result = [1,5,5]")

        print("indef off testing-----------------------------------------------")
        points = [[[1,2]],[[3,4]],[[6,8]],[[5,8]],[[7,8]],[[9,10]],[[11,12]]]
        pointa = [3,4]
        pointb = [7,12]
        print("pointa =",pointa)
        print("pointb =",pointb)
        print("Result =",self.indexOf(pointa,points))
        print("Expected Result = 1")
        print("Result =",self.indexOf(pointb,points))
        print("Expected Result = -1")
        
    """
        make an line equation for two given point
        it returns a array containg the slope of the line and 
        the y intercept
    """
    def LinerEquation(self,point1,point2):
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        '''
            if both of the x are same then slope is infinity
        '''
        if(x1==x2):
            return [[0,x1]]
        else:   
            b=(x2*y1-x1*y2)/(x2-x1)
            a = (y2-b)/x2
            return [[a,b]]

    """
        Calculates the number of points in approx array between
        point startpoint and endpoint
        it return an array of with the index after the startpoint index and
        a index before the endpoint index and the number of points in between
    """
    def NumberOfPointInBetween(self,startpoint,endpoint,approx):

        startIndex = -1
        endIndex = -1 
        count=0

        #getting the index of the startpoint and endpoint in approx
        for check in range(0,len(approx)):
            startPoint=approx[check]
            if(startPoint[0][0] == startpoint[0]  and startPoint[0][1] == startpoint[1]):
                startIndex = check
        for check in range(0,len(approx)):
            startPoint=approx[check]
            if(startPoint[0][0] == endpoint[0]  and startPoint[0][1] == endpoint[1]):
                endIndex=check
                break
        if(startIndex ==-1 or endIndex == -1):
            return [-1,-1,-1]
        #getting the index of point after the startpoint and
        #getting the index of point before the endpoint 
        startIndex = startIndex+1
        startCheck = startIndex
        endCheck = endIndex-1
        if(endCheck<0):
            endCheck=len(approx)-1
        if(startIndex>=len(approx)):
            startIndex = 0
        startCheck = startIndex

        #counting the number of points
        while(startIndex!=endIndex):
            count=count+1
            startIndex=startIndex+1
            if(startIndex>=len(approx)):
                startIndex=0
        return [startCheck,endCheck,count]
    
    """
        gets the index of the points in approx
    """
    def indexOf(self,point,approx):
        index = -1
        for check in range(0,len(approx)):
            startPoint=approx[check]
            if(startPoint[0][0] == point[0]  and startPoint[0][1] == point[1]):
                index = check
                break
        return index
    """
        Check if the point from startcheck and endcheck in approx 
        can be a curve or not
    """
    def CheckForCurve(self,startCheck,endCheck,approx, opsite=False):
        #get the equation for the index startcheck and endcheck in array approx
        Eq = self.LinerEquation([ approx[startCheck][0][0] , approx[startCheck][0][1] ] , [ approx[endCheck][0][0] , approx[endCheck][0][1] ])
        nextPointCheck=0

        if(startCheck+1< len(approx)):
            nextPointCheck = approx[startCheck+1]
        else:
            nextPointCheck = approx[0]
        y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
        angle = math.atan2(approx[endCheck][0][1] - approx[startCheck][0][1], approx[endCheck][0][0] - approx[startCheck][0][0]) * 180.0 / math.pi

        # checking if the eqution is in Y direction or X direction
        isY = True
        if((-135<=angle and angle<=-45) or (45<=angle and angle<=135)):
            isY = False
    
        above = False   
        x=0    

        #check if the curve is convex or concave
        if(y<nextPointCheck[0][1] and isY):
            above = False   
        else:
            if(not isY):
                x=0
                if(Eq[0][0]==0):
                    x = approx[endCheck][0][0]
                else:
                    x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
                if(x>nextPointCheck[0][0]):
                    above = True   
                else:
                    above = False
            else:
                above = True
        startIndex = startCheck 
        endIndex = endCheck
        if(opsite):
            vaildPoint = False
        else:
            vaildPoint = True

        # checking if all the points from startcheck to endcheck 
        # are in the same direction as in the first point
        # if they are not in same direction then the startpoint and checkpoint 
        # cannot create a curve
        while(startIndex!=endIndex):
            while(endIndex!=startIndex):
                Eq = self.LinerEquation([ approx[startIndex][0][0] , approx[startIndex][0][1] ] , [ approx[endIndex][0][0] , approx[endIndex][0][1] ])
                check = startIndex+1
                if(check>=len(approx)):
                    check=0
                while(check!=endIndex):
                    nextPointCheck = approx[check]
                    y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
                    x = 0
                    if(Eq[0][0]!=0):
                        x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
                    else:
                        x = approx[startIndex][0][0]
                    if(not isY):
                        if(above and nextPointCheck[0][0]>x):
                            if(opsite):
                                vaildPoint = True
                            else:
                                vaildPoint = False
                        if(not above and nextPointCheck[0][0]<x):
                            if(opsite):
                                vaildPoint = True
                            else:
                                vaildPoint = False
                    if(above and nextPointCheck[0][1]>y and isY):
                            if(opsite):
                                vaildPoint = True
                            else:
                                vaildPoint = False
                    if(not above and nextPointCheck[0][1]<y and isY):
                            if(opsite):
                                vaildPoint = True
                            else:
                                vaildPoint = False
                    check=check+1
                    
                    if(check>=len(approx)):
                        check=0
                endIndex=endIndex-1
                if(endIndex<0):
                    endIndex=len(approx)-1
            startIndex=startIndex+1
            if(startIndex>=len(approx)):
                startIndex=0
            endIndex=endCheck
    
        return vaildPoint

    """
        find the four corners for the piece and set the each edge of the piece
    """
    def findingcorners(self):
            #getting the pieces of jigsaw
            tmpim=self.image
            #denosing the image of each piece (Actually one piece)
            dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
            #convertinf it into grayscale image
            gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
            #making the threshold of the grayscaled image
            ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
            #dectecting the contours of the pieces    
            im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
            #self.setPoints(contoursPi)
            #using approximate shape of the contour
            newImageAppro = np.zeros_like(tmpim)
            Directions=[]
            var=contoursPi[0]
            epsilon = 0.014*cv2.arcLength(var,True)
            approx = cv2.approxPolyDP(var,epsilon,True)
            for varCo in range(0,len(approx)-1):
                varCord = approx[varCo]
                varCord2 = approx[varCo+1]
                cv2.line(newImageAppro,(varCord[0][0],varCord[0][1]),(varCord2[0][0],varCord2[0][1]), (255,255,255), 1)
            cv2.line(newImageAppro,(approx[0][0][0],approx[0][0][1]),(approx[len(approx)-1][0][0],approx[len(approx)-1][0][1]), (255,255,255), 1)

            #create a blob for detecting the centre of the piece
            params = cv2.SimpleBlobDetector_Params()
                ## Change thresholds
            params.minThreshold = 230
            params.maxThreshold = 255
                
                
                ## Filter by Area.
            params.filterByArea = False
            params.minArea = 1500
                
                ## Filter by Circularity
            params.filterByCircularity = False
            params.minCircularity = 0.1
                
                ## Filter by Convexity
            params.filterByConvexity = False
            params.minConvexity = 0.87
                
                ## Filter by Inertia
            params.filterByInertia = False
            params.minInertiaRatio = 0.01
                
                ## Create a detector with the parameters
            detector = cv2.SimpleBlobDetector_create(params)
                ## Detect blobs.
            keypoints = detector.detect(newImageAppro)
        
                ## Draw detected blobs as red circles.
                ## cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
                ## the size of the circle corresponds to the size of blob
                
            im_with_keypoints = cv2.drawKeypoints(tmpim, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            centerX=0
            centerY=0
            #storing the centre of the piece
            for keyPoint in keypoints:
                x = keyPoint.pt[0]
                y = keyPoint.pt[1]
                centerX = x
                centerY = y
           
            #getting all the set of possible corner points        
            Possible_Corners=[]
            cornerFound = False
            for point in range(0,len(approx)):    
                isPointCorner = approx[point]
                startPoint = point+1
                UppperR = False
                UppperL = False
                LowwerR = False
                LowwerL = False
                while point!=startPoint:       
                    if(startPoint>=len(approx)):
                        startPoint = 0
                    nextPoint = approx[startPoint]
                    #checking in which direction is the point in reference to startPoint
                    if(point!=startPoint):
                        angle = math.atan2(nextPoint[0][1] - isPointCorner[0][1], nextPoint[0][0] - isPointCorner[0][0]) * 180.0 / math.pi
                        if(angle>=0 and angle <=90):
                            UppperR = True
                        if(angle>90 and angle <=180):
                            UppperL = True
                        if(angle<0 and angle >=-90):
                            LowwerR = True
                        if(angle<-90 and angle >=-180):
                            LowwerL = True
                        startPoint=startPoint+1
                # if a point startPoint has a point in ever direction then it cannot be a corner
                if((UppperR and UppperL and LowwerR and LowwerL)==False):
                    Possible_Corners.append([isPointCorner[0][0],isPointCorner[0][1]])
           
        #finding all corners
            for i in range(0,len(Possible_Corners)):
                #assuming that i index point is the corner
                if(cornerFound):
                    break
                cornerOne = Possible_Corners[i]
        #------------------------------------------------------------------
        #second corner point finding
                j=i+1
                
                if(j>=len(Possible_Corners)):
                    j=0
                while(j!=i):
                    #assuming that j index point is the corner
                    if(j >= len(Possible_Corners)):
                        j=0
                    if(j == i):
                        # if j is equal to i then we have check all the points thus i cannot be a corner
                        break
                    cornerTwo = Possible_Corners[j]
                    returnedpoints = self.NumberOfPointInBetween(cornerOne,cornerTwo,approx)
                    startCheck=returnedpoints[0]
                    endCheck=returnedpoints[1]
                    count=returnedpoints[2]
                    #checking if the point between the two corners are 0 or at least 3
                    if(count == 0 or (count>2)):
                        vaildPoint = True
                        if(count>2):
                            #check if the point are valid meaning that those two point can be a corner
                            vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                            indexI = self.indexOf(cornerOne,approx)
                            indexJ = self.indexOf(cornerTwo,approx)
                        if(vaildPoint and self.isCorner(cornerOne, approx[startCheck][0],approx[endCheck][0],cornerTwo)):
                            #if it is vaild then find the third corner
                            #----------------------------------------------------------------------------
                            #Third corner point finding
                            k=j+1
                            if(k>=len(Possible_Corners)):
                                k=0
                            while(k!=i):
                                if(k >= len(Possible_Corners)):
                                    k=0
                                if(k == i):
                                    # if k is equal to i then we have check all the points thus j cannot be a corner
                                    break
                                cornerThree=Possible_Corners[k]
                                returnedpoints = self.NumberOfPointInBetween(cornerTwo,cornerThree,approx)
                                startCheck=returnedpoints[0]
                                endCheck=returnedpoints[1]
                                count=returnedpoints[2]
                                if(count == 0 or (count>2)):
                                    #if the number of points in between the corner is 0 or more than 2 then 
                                    #it can be corner
                                    vaildPoint = True
                                    if(count>2):
                                        #check if the point are valid for been the corner
                                        vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                        # if cornerone and cornertwo had 3 number of point then try to find a point between j and k which make be a cornertwo
                                        # if such a point can be found then j is not a corner
                                        if( self.NumberOfPointInBetween(cornerOne,cornerTwo,approx)[2] == 3  and vaildPoint):
                                            flag=True
                                            dvi = j+1
                                            while(dvi !=k):
                                                if(dvi >= len(Possible_Corners)):
                                                    dvi = 0
                                                possibleCornerthree = Possible_Corners[dvi]
                                                posreturnedpoints = self.NumberOfPointInBetween(cornerOne,possibleCornerthree,approx)
                                                posstartCheck=returnedpoints[0]
                                                posendCheck=returnedpoints[1]
                                                poscount=returnedpoints[2]
                                                posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                if(posvaildPoint):
                                                    flag = False
                                                dvi=dvi+1
                                                if(dvi >= len(Possible_Corners)):
                                                    dvi = 0
                                            vaildPoint = flag

                                        indexK = self.indexOf(cornerThree,approx)
                                        indexJ = self.indexOf(cornerTwo,approx)
                                    if(vaildPoint and self.isCorner(cornerTwo, approx[startCheck][0],approx[endCheck][0],cornerThree)):
                                    #-------------------------------------------------------------------------------------------------------
                                    #fourth point corner dectection
                                        l=k+1
                                        if(l >= len(Possible_Corners)):
                                            l=0
                                        while(l!=i):
                                            if(l >= len(Possible_Corners)):
                                                l=0
                                            if(l == i):
                                                # if l is equal to i then we have check all the points thus k cannot be a corner
                                                break
                                            cornerFour = Possible_Corners[l]
                                            returnedpoints = self.NumberOfPointInBetween(cornerThree,cornerFour,approx)
                                            startCheck=returnedpoints[0]
                                            endCheck=returnedpoints[1]
                                            count=returnedpoints[2]
                                            if(count==0 or (count>2)):
                                                #got four point which are valid for corner but it could be that they are not
                                                vaildPoint = True
                                                if(count>2):
                                                    #check if the point are valid meaning that those two point can be a corner
                                                    vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                    # if cornerTwo and cornerThree had 3 number of point then try to find a point between k and l which make be a cornerthree
                                                    # if such a point can be found then k is not a corner
                                                    if( self.NumberOfPointInBetween(cornerTwo,cornerThree,approx)[2] == 3  and vaildPoint):
                                                                    flag=True
                                                                    dvi = k+1
                                                                    while(dvi !=l ):
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                        possibleCornerthree = Possible_Corners[dvi]
                                                                        posreturnedpoints = self.NumberOfPointInBetween(cornerTwo,possibleCornerthree,approx)
                                                                        posstartCheck=returnedpoints[0]
                                                                        posendCheck=returnedpoints[1]
                                                                        poscount=returnedpoints[2]
                                                                        posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                                        if(posvaildPoint):
                                                                            flag = False
                                                                        dvi=dvi+1
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                    vaildPoint = flag
                                                    indexK = self.indexOf(cornerThree,approx)
                                                    indexL = self.indexOf(cornerFour,approx)
                                                if(vaildPoint and self.isCorner(cornerThree, approx[startCheck][0],approx[endCheck][0],cornerFour)):
                                                    vaildPoint = True
                                                    
                                                    if(vaildPoint):

                                                
                                                        returnedpoints = self.NumberOfPointInBetween(cornerFour,cornerOne,approx)
                                                        startCheck=returnedpoints[0]
                                                        endCheck=returnedpoints[1]
                                                        count=returnedpoints[2]
                                                        if(count == 0 or (count>2)):
                                                           
                                                            
                                                            vaildPoint = True
                                                            angle5=0
                                                            angle6=0
                                                            if(count>2):
                                                                # if cornerThree and cornerFour had 3 number of point then try to find a point between l and i which make be a cornerFour
                                                                # if such a point can be found then l is not a corner

                                                                vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                                if( self.NumberOfPointInBetween(cornerThree,cornerFour,approx)[2] == 3  and vaildPoint):
                                                                    flag=True
                                                                    dvi = l+1
                                                                    while(dvi !=i ):
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                        possibleCornertwo = Possible_Corners[dvi]
                                                                        posreturnedpoints = self.NumberOfPointInBetween(cornerThree,possibleCornertwo,approx)
                                                                        posstartCheck=returnedpoints[0]
                                                                        posendCheck=returnedpoints[1]
                                                                        poscount=returnedpoints[2]
                                                                        posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                                        if(posvaildPoint):
                                                                            flag = False
                                                                        dvi=dvi+1
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                    vaildPoint = flag
                                                                indexI = self.indexOf(cornerOne,approx)
                                                                indexL = self.indexOf(cornerFour,approx)
                                                            if(vaildPoint and self.isCorner(cornerFour, approx[startCheck][0],approx[endCheck][0],cornerOne)):
                                                                p = path.Path([(cornerOne[0],cornerOne[1])
                                                                                        , (cornerTwo[0], cornerTwo[1]), (cornerThree[0], cornerThree[1]), (cornerFour[0], cornerFour[1])])
                                                                result = p.contains_points([(centerX, centerY)])
                                                                # checking if the center is still in the center of the four corner found
                                                                if(result[0]):
                                                                    #storing the corner
                                                                    self.corners.append(cornerOne)
                                                                    self.corners.append(cornerTwo)
                                                                    self.corners.append(cornerThree)
                                                                    self.corners.append(cornerFour)
                                                                    cornerFound = True
                                            #
                                            #if the corner is found then break all the loop
                                            #    
                                            if(cornerFound):
                                                break    
                                            l=l+1
                                if(cornerFound):
                                    break   
                                k=k+1
                    if(cornerFound):
                        break
                    j=j+1
            if(self.corners == []):
                return "CORNER_NOT_FOUND"
            

            #storing the center of the piece and setting the four edge of the piece
            self.center.append(centerX)
            self.center.append(centerY)
            self.setPropertyOfCorner(approx,contoursPi)
            return "COMPLETE"




        

    """
       approx -- all the approx rectanguler points
       contours -- contains all the points in the pieces
       pointA -- one corner in this side on approx array
       pointB -- second corner in this side on approx array
       startPoint -- one corner in this side on allpoints array
       endPoint -- second corner in this side on allpoints array
       allpoints -- contains all the points on the side of this piece
    """
    def getSide(self, approx, contours, pointA, pointB, startPoint, endPoint,allPoints):
        side=sideOfPieces(pointA,pointB)
        indexI = self.indexOf(pointA,approx)
        indexJ = self.indexOf(pointB,approx)
        pointBetweenAB =  self.NumberOfPointInBetween(pointA,pointB,approx)[2]
        points=[]
        if(pointBetweenAB==0):
            #if the number of point is zero in between then it is a straight line
            points.append(pointA)
            points.append(pointB)
            side.isStraight = True
        if(pointBetweenAB!=0):
            #if the corners have a curve

            #setting all the points
            points = self.getPointsForApprox(allPoints,startPoint,endPoint)
            
            #checking if the curve is a convex and concave
            nextPoint = indexI+1
            if(nextPoint>=len(approx)):
                nextPoint = 0
            previousPoint = indexJ-1
            if(previousPoint < 0):
                previousPoint = len(approx)-1
            
            Eq = self.LinerEquation([ approx[nextPoint][0][0] , approx[nextPoint][0][1] ] , [ approx[previousPoint][0][0] , approx[previousPoint][0][1] ])
            nextPointCheck=0
            if(nextPoint+1< len(approx)):
                nextPointCheck = approx[nextPoint+1]
            else:
                nextPointCheck = approx[0]
            y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
            angle = math.atan2(approx[previousPoint][0][1] - approx[nextPoint][0][1], approx[previousPoint][0][0] - approx[nextPoint][0][0]) * 180.0 / math.pi
            # We are lookin into y because y is different on the equation and different for the actual points
            # thus we look into y when the degree is between -135 and -45 ot 45 and 135
            isY = True
            if((-135<=angle and angle<=-45) or (45<=angle and angle<=135)):
                isY = False 
            #checking if the point is in convex or concave range
            above = False   
            x=0    
            if(y<nextPointCheck[0][1] and isY):
                above = False   
            else:
                if(not isY):
                    x=0
                    if(Eq[0][0]==0):
                        x = approx[previousPoint][0][0]
                    else:
                        x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
                    if(x>nextPointCheck[0][0]):
                        above = True    
                    else:
                        above = False
                else:
                    above = True
            
            #setting if the edge is a convex concave
            if(isY):
                y = Eq[0][0] * self.center[0]+ Eq[0][1]
                if(y<self.center[1] and  not above):
                    side.isConvex=True 
                elif(y>self.center[1] and above):
                    side.isConvex=True 
                else:
                    side.isConcave=True 
            else:
                x=0
                if(Eq[0][0]==0):
                    x = approx[previousPoint][0][0]
                else:
                    x = (self.center[1]-Eq[0][1])/Eq[0][0]

                if(x<self.center[0] and  not above):
                    side.isConvex=True
                elif(x>self.center[0] and above):
                    side.isConvex=True
                else:
                    side.isConcave=True
        #storing the original points of the side
        side.originalPoints = points
            
        return side
    
    """
        return a array containing the points from startpoint till endpoint in approx
    """
    def getPointsForApprox(self, approx, startPoint, endPoint):
        points = []
        cordinate = approx[startPoint]
        #adding the first points 
        points.append([cordinate[0][0],cordinate[0][1]])
        while(startPoint != endPoint):
            ipoint = startPoint + 1
            if(ipoint != endPoint and not ipoint>=len(approx)):
                cordinate = approx[ipoint]
                points.append([cordinate[0][0],cordinate[0][1]])
            if(ipoint>=len(approx)):
                #if the point is more then the length then make it 0
                startPoint = 0
            else:
                startPoint = ipoint
        cordinate = approx[endPoint]
        points.append([cordinate[0][0],cordinate[0][1]])
        return points 

    """
        sets the property of the piece
        creates new side and add it to the side array of the piece
    """
    def setPropertyOfCorner(self ,approx, contours):
        cornerA = self.corners[0]
        cornerB = self.corners[1]
        cornerC = self.corners[2]
        cornerD = self.corners[3]
        
        #getting the number of point between each edge
        pointBetweenAB =  self.NumberOfPointInBetween(cornerA,cornerB,approx)[2]
        pointBetweenBC =  self.NumberOfPointInBetween(cornerB,cornerC,approx)[2]
        pointBetweenCD =  self.NumberOfPointInBetween(cornerC,cornerD,approx)[2]
        pointBetweenDA =  self.NumberOfPointInBetween(cornerD,cornerA,approx)[2]

        #getting the position of the corner in approx
        pointi = self.indexOf(cornerA,approx)
        pointj = self.indexOf(cornerB,approx)
        pointk = self.indexOf(cornerC,approx)
        pointl = self.indexOf(cornerD,approx)

        #all the points between the corners in approx
        approxPointA = self.getPointsForApprox(approx,pointi,pointj)
        approxPointB = self.getPointsForApprox(approx,pointj,pointk)
        approxPointC = self.getPointsForApprox(approx,pointk,pointl)
        approxPointD = self.getPointsForApprox(approx,pointl,pointi)
        
        #decideing if the pieces is a corner, border or an center piece
        if(pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0):
            self.isCenterPiece = True
        elif((pointBetweenAB == 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
            or (pointBetweenAB != 0 and pointBetweenBC == 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
                or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD == 0 and pointBetweenDA != 0)
                    or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA == 0)):
            self.isBorderPiece = True
        else:
            self.isCornerPiece = True

        #here we are trying to find the best match for the corner in the contours
        #-1 indecates if the match is not found        
        pointA=-1
        pointB=-1
        pointC=-1
        pointD=-1
        var=contours[0]
        epsilon = 0.0000000001*cv2.arcLength(var,True)
        allPoints = cv2.approxPolyDP(var,epsilon,True)
        for i in range(0,len(allPoints)):
            x = allPoints[i][0][0]
            y = allPoints[i][0][1]
            if(x == cornerA[0] and y == cornerA[1]):
                pointA = i
            if(x == cornerB[0] and y == cornerB[1]):
                pointB = i
            if(x == cornerC[0] and y == cornerC[1]):
                pointC = i
            if(x == cornerD[0] and y == cornerD[1]):
                pointD = i
        #decides if the side is a straight , convex or concave 
        #also store the original point of the graph in the side object
        self.side.append(self.getSide(approx,contours,cornerA,cornerB,pointA,pointB,allPoints))
        self.side.append(self.getSide(approx,contours,cornerB,cornerC,pointB,pointC,allPoints))
        self.side.append(self.getSide(approx,contours,cornerC,cornerD,pointC,pointD,allPoints))
        self.side.append(self.getSide(approx,contours,cornerD,cornerA,pointD,pointA,allPoints))

        #store the approximate point of the graph in the side
        self.side[0].approxPoints = approxPointA
        self.side[1].approxPoints = approxPointB
        self.side[2].approxPoints = approxPointC
        self.side[3].approxPoints = approxPointD
    '''
        sets the defination of the side 
        meaning that if the side is on the top 
        it is named TOP if it is at the bottom it is named BOTTOM
        so thi funcition set direction of a side same thing with right and left
    '''
    def setdirection(self):
        axis = self.side[0].whichaxis
        if(axis=="X"):
            #if the side 0 is in x axis then 1 is also in axis and 2 and 3are in y axis
            y1 = self.side[0].cornerRight[1]
            y2 = self.side[2].cornerRight[1]
            #setting if the side 0,2 is bottom or top
            if(y1<y2):
                self.side[0].direction = "TOP"
                self.side[2].direction = "BOTTOM"
            else:
                self.side[0].direction = "BOTTOM"
                self.side[2].direction = "TOP"

            #setting if the side 1,3 is left or right
            x1 = self.side[1].cornerRight[0]
            x2 = self.side[3].cornerRight[0]
            if(x1<x2):
                self.side[1].direction = "LEFT"
                self.side[3].direction = "RIGHT"
            
            else:
                self.side[1].direction = "RIGHT"
                self.side[3].direction = "LEFT"
        else:
            #if the side 0 is in y axis then 1 is also in y axis and 2 and 3 are in x axis
            x1 = self.side[0].cornerRight[0]
            x2 = self.side[2].cornerRight[0]
            #setting if the side 0,2 is left or right
            if(x1<x2):
                self.side[0].direction = "LEFT"
                self.side[2].direction = "RIGHT"
            
            else:
                self.side[0].direction = "RIGHT"
                self.side[2].direction = "LEFT"
            #setting if the side 1,3 is bottom or top

            y1 = self.side[1].cornerRight[1]
            y2 = self.side[3].cornerRight[1]
            if(y1<y2):
                self.side[1].direction = "TOP"
                self.side[3].direction = "BOTTOM"
            
            else:
                self.side[1].direction = "BOTTOM"
                self.side[3].direction = "TOP"
        sidea = self.side[0]
        sideb = self.side[1]
        sidec = self.side[2]
        sided = self.side[3]

        #giving the name to the piece
        #TL means top left
        #TR means top right 
        #BL means bottom left 
        #BR means bottom right 
        # or N if no match could be found
        if(((sidea.isStraight and sidea.direction=="TOP") or (sidec.isStraight and sidec.direction=="TOP") 
                or (sideb.isStraight and sideb.direction=="TOP") or (sided.isStraight and sided.direction=="TOP"))
    
                and ((sidea.isStraight and sidea.direction=="LEFT") or (sidec.isStraight and sidec.direction=="LEFT") 
                or (sideb.isStraight and sideb.direction=="LEFT") or (sided.isStraight and sided.direction=="LEFT"))):
            self.name = "TL"
        elif(((sidea.isStraight and sidea.direction=="TOP") or (sidec.isStraight and sidec.direction=="TOP") 
                or (sideb.isStraight and sideb.direction=="TOP") or (sided.isStraight and sided.direction=="TOP"))
    
                and ((sidea.isStraight and sidea.direction=="RIGHT") or (sidec.isStraight and sidec.direction=="RIGHT") 
                or (sideb.isStraight and sideb.direction=="RIGHT") or (sided.isStraight and sided.direction=="RIGHT"))):
            self.name = "TR"
        elif(((sidea.isStraight and sidea.direction=="BOTTOM") or (sidec.isStraight and sidec.direction=="BOTTOM") 
                or (sideb.isStraight and sideb.direction=="BOTTOM") or (sided.isStraight and sided.direction=="BOTTOM"))

                and ((sidea.isStraight and sidea.direction=="LEFT") or (sidec.isStraight and sidec.direction=="LEFT") 
                or (sideb.isStraight and sideb.direction=="LEFT") or (sided.isStraight and sided.direction=="LEFT"))):
            self.name = "BL"
        elif(((sidea.isStraight and sidea.direction=="BOTTOM") or (sidec.isStraight and sidec.direction=="BOTTOM") 
                or (sideb.isStraight and sideb.direction=="BOTTOM") or (sided.isStraight and sided.direction=="BOTTOM"))
    
                and ((sidea.isStraight and sidea.direction=="RIGHT") or (sidec.isStraight and sidec.direction=="RIGHT") 
                or (sideb.isStraight and sideb.direction=="RIGHT") or (sided.isStraight and sided.direction=="RIGHT"))):
            self.name = "BR"
        else:
            self.name = "N"
            

   



    """
        retuns the distance between two points
    """
    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5
    """
        gets two point and then calclutes the angle between them
        and returns the angle in 0 -360
    """
    def getAngle(self,pointA,pointB):
        angle = math.atan2(pointB[1] - pointA[1], pointB[0] - pointA[0]) * 180.0 / math.pi
        newAngle = angle
        if(angle<0):
            newAngle = angle *-1
        elif(angle != 0):
            newAngle = 360 -angle
        else:
            if(pointB[0]<pointA[0]):
                newAngle = 180
            else:
                newAngle = 0
        return newAngle

    """
        checks if the pointa, nextpoint and prevpoint and pointb have nearly the same angle or not
        this is done through doing the section on angle
    """
    def isCorner(self,pointa,nextpoint,prevpoint,pointb):
        anglea = self.getAngle(pointa,nextpoint)
        angleb = self.getAngle(prevpoint,pointb)
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            return True
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return True
        else:
            return False
    """
        Extracts the colour range from the piece and then each side is given a colour
    """
    def extractColour(self):
            tmpim=self.image
            #denosing the image of each piece (Actually one piece)
            dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
            #convert it into grayscale image
            gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
            #making the threshold of the grayscaled image
            ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
            #dectecting the contours of the pieces    
            im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
            
            var=contoursPi[0]
            intensities = []

            cimg12 = np.zeros_like(tmpim)
            cv2.drawContours(cimg12, contoursPi, 0, color=255, thickness=12)
            pts12 = np.where(cimg12 == 255)

            cimg_1 = np.zeros_like(tmpim)
            cv2.drawContours(cimg_1, contoursPi, 0, color=255, thickness=-5)
            pts_1 = np.where(cimg_1 == 255)

            cimg13 = np.zeros_like(tmpim)
            cv2.drawContours(cimg13, contoursPi, 0, color=255, thickness=13)
            pts13 = np.where(cimg13 == 255)

            #rearraging the points
            pts_1 = self.arrangethepoints(pts_1)
            pts13 = self.arrangethepoints(pts13)
            pts12 = self.arrangethepoints(pts12)

            #removing the points which does not have the colour and the points which are extra
            pts15  = [x for x in pts13 if not x in pts12 and x in pts_1]
            
            #creating an image for the extrated points 
            testing = np.zeros_like(tmpim)
            for i in range(0,len(pts15)):
                cv2.circle(testing,(int(pts15[i][1]),int(pts15[i][0])), 1, (255,255,255), 1)
            
            #using contours to get the location of extracted point in an order
            gryPiec = cv2.cvtColor(testing,cv2.COLOR_RGB2GRAY)
            ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY)
            im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)

            #seeting each colour which has been extracted to a side
            sidea =self.getside("TOP")[0]
            if(not sidea.isStraight):
                self.setcolour(sidea,contoursPi)
            sidea =self.getside("BOTTOM")[0]
            if(not sidea.isStraight):
                self.setcolour(sidea,contoursPi)
            sidea =self.getside("RIGHT")[0]
            if(not sidea.isStraight):
                self.setcolour(sidea,contoursPi)
            sidea =self.getside("LEFT")[0]
            if(not sidea.isStraight):
                self.setcolour(sidea,contoursPi)

    """
        set the colour for the edge which has been sent to the function
    """
    def setcolour(self,sidea,contoursPi):       
            cornerR = sidea.cornerRight
            cornerL = sidea.cornerLeft
            start = []
            end = []
            stat = 0
            end2 = 0
            #calculates the distance of each point from the sides corner
            for i in range(0,len(contoursPi[0])):
                point = contoursPi[0][i][0]
                start.append(self.getDistance(point,[cornerR[0],cornerR[1]]))
                end.append(self.getDistance(point,[cornerL[0],cornerL[1]]))

                if(start[stat] > start[i]):
                    stat = i
                if(end[end2] > end[i]):
                    end2 = i

            points = []
            # finding the closet points to the corner
            # which would be the new points of the colour array
            while(stat!=end2):
                points.append(contoursPi[0][stat][0])
                stat = stat+1
                if(stat>=len(contoursPi[0])):
                    stat=0
    
            #subsampling the colour extracted points according to the axis in which the side is
            newpoints = []
            if(sidea.whichaxis == "X"):
                newpoints=sidea.subsamplingxaxis(points)
            elif(sidea.whichaxis == "Y"):
                newpoints=sidea.subsamplingyaxis(points)

            newpoints = sidea.arrangethepoints(newpoints)

            #contourbgr= np.zeros_like(self.image)
            #self.showImage("REAL ONE")

            #extracting the colour from the location and then storing in sides
            colour = []
            for i in range(0,len(newpoints)):
                pot = newpoints[i]
                b = int(self.image[pot[1]][pot[0]][0])
                g = int(self.image[pot[1]][pot[0]][1])
                r = int(self.image[pot[1]][pot[0]][2])
                colour.append([b,g,r])
            sidea.colour = colour
            sidea.colourreverse = colour[::-1]
    
    """
        find the side in piece which has the direction as given 
        piece : piece of the jigsaw puzzle
        direction : the direction of the side should be same
    """
    def getside(self,direction):
        # getting all the side of the piece
        sidea = self.side[0]
        sideb = self.side[1]
        sidec = self.side[2]
        sided = self.side[3]
        #checking which direction it is and returning the side
        if(sidea.direction == direction):  
            return [sidea,0]
        if(sideb.direction == direction):  
            return [sideb,1]
        if(sidec.direction == direction): 
            return [sidec,2]
        if(sided.direction == direction): 
            return [sided,3]
    def arrangethepoints(self,pointa):
        point = []
        for i in range(0,len(pointa[0])):       
            point.append([pointa[0][i],pointa[1][i]])
        return point


    def showImage(self,name):

            tmpim=self.image
            cv2.imshow(name,tmpim)
test = False
if(test):
    test = pieces()
    test.unittestingfunction()