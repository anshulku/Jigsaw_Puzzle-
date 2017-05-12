import cv2
import numpy as np;
import math
# read the image throught an window frame 
#imports for that
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
from sympy import pi,mpmath

class sideOfPieces:
    def __init__(self,right,left):
        self.contourpoints = []
        self.x_axis_Points=[]
        self.x_axis_PointsApprox = []

        self.x_subampledpoints = []
        self.y_subampledpoints = []

        self.pointsStart = []
        self.pointsEnd = []

        #not going to use any more

        self.cornerRight=right
        self.cornerLeft=left
        self.curvecenter = []
        #point iam using now
        self.approxPoints = []
        self.originalPoints=[]
        self.isStraight = False
        self.isConvex = False
        self.isConcave = False
        self.approxmatchside = []
        self.axismatchside = []
        self.axismatchsidereverse = []
        self.whichaxis = ""
        self.lengthofside = 0
        self.aboveorbelow = True
        self.samplept = []
        self.sampleptreverse = []
        self.direction = ""
        self.colour = []
        self.colourreverse = []
    
    """
        gets the minimum point among the corner
    """
    def getmincornerpoint(self):
        # if the axis is x then the min is which one has smaller x
        # otherwise it is with min y
        if(self.whichaxis == "X"):
            if( self.cornerRight[0] < self.cornerLeft[0]):
                return self.cornerRight
            else:
                return self.cornerLeft
        else:
            if( self.cornerRight[1] < self.cornerLeft[1]):
                return self.cornerRight
            else:
                return self.cornerLeft
    """
        gets the maxmimum point among the corner
    """
    def getmaxcornerpoint(self):
        # if the axis is x then the max is which one has larger x
        # otherwise it is with max y
        if(self.whichaxis == "X"):
            if( self.cornerRight[0] < self.cornerLeft[0]):
                return self.cornerLeft
            else:
                return self.cornerRight
        else:
            if( self.cornerRight[1] < self.cornerLeft[1]):
                return self.cornerLeft
            else:
                return self.cornerRight
    

    """
        apepend all the point from pointA to pointB
        the appending is done in reverse if the reverseAdd is true
    """
    def appendpoint(self,pointA, pointB, reverseAdd = False):
        start = 0
        end = len(pointA)
        increment = 1
        if(reverseAdd):
            start = len(pointA)-1
            end = -1
            increment = -1
        for i in range(start, end, increment):
            pointB.append(pointA[i])
    """
        get the angle between the two point
        The angle return is between 0 and 360
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
         transforms the graph from given set to the start location of x,y
    """
    def transform(self,points,x,y):
        originAngle = (self.getAngle(points[0],points[len(points)-1]))
        newFirstX = x
        newFirstY = y
        newPoints = [[newFirstX,newFirstY]]
        point1 = points[0]
        for i in range(1,len(points)):
            point2 = points[i]
            angle = (self.getAngle(point1,point2))
            distance = self.getDistance(point1,point2)
            newX = newFirstX + (distance * math.cos(math.radians(-angle)))
            newY = newFirstY + (distance * math.sin(math.radians(-angle)))
            newPoints.append([newX,newY])
        return newPoints
    """
        store the tranformed points of the edge
    """
    def transformedge(self):
            self.axismatchside = self.transform(self.originalPoints,200,200)
            point = []
            for i in range(len(self.originalPoints)-1,-1,-1):
                point.append(self.originalPoints[i])
            self.axismatchsidereverse =  self.transform(point,200,200)
            self.approxmatchside = self.transform(self.approxPoints,200,200)
            
            return self.approxmatchside
    """
        checks if the two angle send can have a match for a piece or not
    """
    def samesection(self,anglea):
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            return [True,"X"]
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return [True,"Y"]
        else:
            return [False]
    """
        make the liner eqution for given two points
        return an array in which the first position contains the slope         
         and the second position contains the constant 
        if the line is on 90 degree then it return 0 and the x cordinate with it 
    """
    def linerEquation(self,pointa,pointb):
        x1 = pointa[0]
        y1 = pointa[1]
        x2 = pointb[0]
        y2 = pointb[1]
        m = 0 
        c = x1
        if(not x1 == x2):
            c = (x2*y1-x1*y2)/(x2-x1)
            m = (y2-c)/x2
            if(m==0):
                c = y1

        return [m,c]
    """
     return the number between pointa and point b
    """
    def getrange(self,pointa,pointb):
        start = int(min(pointa,pointb))
        end = int(max(pointa,pointb))
        x = []
        for i in range(start,end):
            x.append(i)
        if(start==end):
            return [[start],False]
        return [x,start==pointa]
    """
        subsamples the data across x axis
    """ 
    def subsamplingxaxis(self,side):
        x = []
        y = []
        for i in range(0,len(side)-1):
            pointa = [int(side[i][0]),int(side[i][1])]
            pointb = [int(side[i+1][0]),int(side[i+1][1])]
            eq = self.linerEquation(pointa,pointb)
            rangexside = self.getrange(pointa[0],pointb[0])
            rangex = rangexside[0]
            rangey = []
            if(eq[0]==0):
                if(eq[1]==pointa[1]):  #meaning that the constant is y so the slope is zero
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
                elif(eq[1]==pointa[0]): #meaning that the constant is x so the slope is infinty
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
            else:
                    for j in range(0,len(rangex)):
                        rangey.append(eq[0]*rangex[j] + eq[1])

            if(rangexside[1]):
                 for j in range(0,len(rangex)):
                    x.append(rangex[j])
                    y.append(rangey[j])
            else:
                 for j in range(len(rangex)-1,-1,-1):
                    x.append(rangex[j])
                    y.append(rangey[j])
                
            
        return [x,y]
    """
        subsamples the data across y axis
    """
    def subsamplingyaxis(self,side):
        x = []
        y = []
        for i in range(0,len(side)-1):
            pointa = [int(side[i][0]),int(side[i][1])]
            pointb = [int(side[i+1][0]),int(side[i+1][1])]
            eq = self.linerEquation(pointa,pointb)
            rangexside = self.getrange(pointa[1],pointb[1])
            rangey = rangexside[0]
            rangex = []
            if(eq[0]==0):
                if(eq[1]==pointa[1]):  #meaning that the constant is y so the slope is zero
                    for j in range(0,len(rangey)):
                        rangex.append(pointa[0])
                elif(eq[1]==pointa[0]): #meaning that the constant is x so the slope is infinty
                    for j in range(0,len(rangey)):
                        rangex.append(pointa[0])
            else:
                    for j in range(0,len(rangey)):
                        rangex.append((rangey[j]-eq[1])/eq[0])

            if(rangexside[1]):
                 for j in range(0,len(rangey)):
                    x.append(rangex[j])
                    y.append(rangey[j])
            else:
                 for j in range(len(rangey)-1,-1,-1):
                    x.append(rangex[j])
                    y.append(rangey[j])
        return [x,y]
    """
        get the distance of two given points
    """
    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5

    """
        calculates the length of the side 
        and set it to the variable
    """
    def setlength(self):
        length = 0
        for i in range(0,len(self.axismatchside)-1):
            pointa = self.axismatchside[i]
            pointb = self.axismatchside[i+1]
            length = length + self.getDistance(pointa,pointb)
        self.lengthofside = length

    """
        checks if the two angle send can have a match for a piece or not
    """
    def setwhichssection(self,anglea):
        
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225) ):
            self.whichaxis = "X"
        elif((45<anglea<135  or 225<anglea<315)):
            self.whichaxis = "Y"
    
    """
        tell if the graph is going in up direction or in below direction
    """
    def setaboveorbelow(self):
        eq = self.linerEquation(self.approxmatchside[1],self.approxmatchside[len(self.approxmatchside)-2])
        flag = True
        if(self.whichaxis == "X"):
            if(eq[0]==0):
                y = eq[1]
                flag= self.approxmatchside[2][1]<=y
            else:
                y = eq[0]*self.approxmatchside[2][0] + eq[1]
                flag= self.approxmatchside[2][1]<=y
        elif(self.whichaxis == "Y"):
            if(eq[0]==0):
                flag= self.approxmatchside[2][0] < eq[1]
            else:
                x = (self.approxmatchside[2][1]-eq[1])/eq[0]
                flag= self.approxmatchside[2][0] < x
        self.aboveorbelow = flag
    """
        arranges the point from pointa in the right order
    """
    def arrangethepoints(self,pointa):
        point = []
        for i in range(0,len(pointa[0])):       
            point.append([pointa[0][i],pointa[1][i]])
        return point
    def setsubsampling(self):
        pointo = []
        pointreverse = []
        if(self.whichaxis == "X"):
            pointo=self.subsamplingxaxis(self.axismatchside)
            pointreverse=self.subsamplingxaxis(self.axismatchsidereverse)
        elif(self.whichaxis == "Y"):
            pointo=self.subsamplingyaxis(self.axismatchside)
            pointreverse=self.subsamplingyaxis(self.axismatchsidereverse)
        self.samplept = self.arrangethepoints(pointo)
        self.sampleptreverse = self.arrangethepoints(pointreverse)
    

    def testingsubsampling(self,side):
        newImageAppro1 = np.zeros((1000,800,3), np.uint8)
        #print(point)
        #print(pointb)
        for i in range(0,len(self.originalPoints)-1):
            x1 = self.originalPoints[i][0]
            y1 = self.originalPoints[i][1]
            x2 = self.originalPoints[i+1][0]
            y2 = self.originalPoints[i+1][1]
            cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        x = []
        y = []
        for i in range(0,len(side)-1):
            pointa = [int(side[i][0]),int(side[i][1])]
            pointb = [int(side[i+1][0]),int(side[i][1])]
            eq = self.linerEquation(pointa,pointb)
            rangexside = self.getrange(pointa[0],pointb[0])
            rangex = rangexside[0]
            rangey = []
            if(eq[0]==0):
                if(eq[1]==pointa[1]):  #meaning that the constant is y so the slope is zero
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
                elif(eq[1]==pointa[0]): #meaning that the constant is x so the slope is infinty
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
            else:
                    for j in range(0,len(rangex)):
                        rangey.append(eq[0]*rangex[j] + eq[1])
            print("--------------------------------------------------------- = ")
            print("pointa = ",pointa)
            print("pointb = ",pointb)
            print("rangex")
            print(rangex)
            print("rangey")
            print(rangey)
            if(rangexside[1]):
                 for j in range(0,len(rangex)):
                    x.append(rangex[j])
                    y.append(rangey[j])
            else:
                 for j in range(len(rangex)-1,-1,-1):
                    x.append(rangex[j])
                    y.append(rangey[j])
                
            cv2.imshow("TESTING",newImageAppro1)
            cv2.waitKey(0)
        return [x,y]

    """
        sets the neccesary data for matching the pieces
    """
    def setsideproperty(self):
        if(not self.isStraight):
            #make the graph on a specific points
            self.transformedge()
            pointa = self.axismatchside
            angle = self.getAngle(pointa[0],pointa[len(pointa)-1])
            #sets the section of the graph meaning X-axis or Y-axis
            self.setwhichssection(angle)
            #sets the length of the graph
            self.setlength()
            #sets if the side is convex or concave 
            self.setaboveorbelow()
            # samples the data across the section of the original data
            self.setsubsampling()
        if(self.isStraight):
            angle = self.getAngle(self.cornerRight,self.cornerLeft)
            self.setwhichssection(angle)