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
from pieces import pieces
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000



class Result:

    """
        __init__ make the variable needed for the puzzle to be solve
        
    """
    def __init__(self, pieces):
        self.jigsawpieces=pieces
        self.upperleftcorner = None
        self.upperrightcorner = None
        self.lowwerleftcorner = None
        self.lowwerrightcorner = None
        self.useColor = False  
        self.useShape = False
    """
        get the angle between the two point
        The angle return is between 0 and 360
    """
    def getAngle(self,pointA,pointB):
        #getting the angle in respect to x-axis
        angle = math.atan2(pointB[1] - pointA[1], pointB[0] - pointA[0]) * 180.0 / math.pi
        newAngle = angle
        # if the angle is less than 0 then make it positive
        if(angle<0):
            newAngle = angle *-1
        elif(angle != 0):  
            # if the angle is no negative and zero then subtract it from 360
            newAngle = 360 -angle
        else:
            # decide isf it is 180 or 0
            if(pointB[0]<pointA[0]):
                newAngle = 180
            else:
                newAngle = 0
        return newAngle
    
    """
        returns the distance between two point
    """
    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5


    
    """
        decides if the two side can match or not
        this is decided on the basics of that the length and the angle of the side
        this funcition reduces the most number of branch in the tree
    """
    def canmatchAngle(self,sidea,sideb):

        # if the each piece have the angle in different direction 
        # they can't match
        if( not sidea.whichaxis == sideb.whichaxis):
            return False
        
        #if the different between the length of the graph is greater than 10
        #than they are not perfect match
        lengtha = sidea.lengthofside
        lengthb = sideb.lengthofside
        maxlen =max(lengtha,lengthb)
        minlen =min(lengtha,lengthb)
        if(maxlen - minlen > 15):
           return False

        # the two side must be one convex and other concave
        aboveorbelowa = sidea.aboveorbelow
        aboveorbelowb = sideb.aboveorbelow
        if(not aboveorbelowa==aboveorbelowb):
            return False
        return True
    
    """
        find the side in piece which has the direction as given 
        piece : piece of the jigsaw puzzle
        direction : the direction of the side should be same
    """
    def getside(self,piece,direction):
        # getting all the side of the piece
        sidea = piece.side[0]
        sideb = piece.side[1]
        sidec = piece.side[2]
        sided = piece.side[3]
        #checking which direction it is and returning the side
        if(sidea.direction == direction):  
            return [sidea,0]
        if(sideb.direction == direction):  
            return [sideb,1]
        if(sidec.direction == direction): 
            return [sidec,2]
        if(sided.direction == direction): 
            return [sided,3]

    """
        return the solved puzzle
    """
    def getresult(self):
        useColor =True
        useShape = True 
        if(self.useColor or self.useShape):
            useShape = self.useShape
            useColour = self.useColor
        # sets the corner pieces, border pieces and center pieces
        corner = []
        border = []
        center = []
        if(len(self.jigsawpieces)<3):
            return ["PIECE_MISSING"]
        for i in range(0,len(self.jigsawpieces)):
            eachPiece = self.jigsawpieces[i]
            if(eachPiece.isCornerPiece):
                if(eachPiece.name == "TL"): 
                    self.upperleftcorner = eachPiece
                if(eachPiece.name == "TR"):self.upperrightcorner = eachPiece
                if(eachPiece.name == "BL"):self.lowwerleftcorner = eachPiece
                if(eachPiece.name == "BR"):self.lowwerrightcorner = eachPiece
                corner.append(eachPiece)
            if(eachPiece.isBorderPiece):
                border.append(eachPiece)
            if(eachPiece.isCenterPiece):
                center.append(eachPiece)
        if(len(corner)>4):
            return ["MIX_PUZZLE"]
        if(len(corner)<3):
            return ["PIECE_MISSING"]
        # making the corner array arrange in the anti-clockwise order
        cornermatch = [self.upperleftcorner,
                        self.lowwerleftcorner,
                        self.lowwerrightcorner,
                        self.upperrightcorner]
        # setting the flag to true 
        # flag will remain true untill each cycle of start and end
        # start is 0 meaning we start at upperleftcorner 
        # end is 1 meaning we ende at lowwerleftcorner
        # during next interation start will be 1,2,3 and end will be 2,3,0 
        flag = True 
        start = 0
        end = 1
        
        #matchvector contain the piece match of each cycle
        matchvector = []
        while(flag):
            if(end==4):
                #if the end is 4 then making it 0 which mean this is the last cycle
                end=0
            # complete mean that not all pieces match have been found in the specific cycle
            complete = False
            cornerstart = cornermatch[start]
            strsidea = cornerstart.side[0]
            strsideb = cornerstart.side[1]
            strsidec = cornerstart.side[2]
            strsided = cornerstart.side[3]

            #getting the end of the side of the puzzle
            cornerend = cornermatch[end]
            endsidea = cornerend.side[0]
            endsideb = cornerend.side[1]
            endsidec = cornerend.side[2]
            endsided = cornerend.side[3]

            matchside = None
            endmatchside = None
            matchsidei = 0
            endsidei = 0
            '''
                getting which side is to be match for the startcorner 
                also getting the end side for the endcorner
                and storing the index of the end side to be matched
            '''
            if(cornerstart.name=="TL"):
                sideachieved = self.getside(cornerstart,"BOTTOM")
                matchside = sideachieved[0]
                sideachieved = self.getside(cornerend,"TOP")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="BL"):
                sideachieved = self.getside(cornerstart,"RIGHT")
                matchside = sideachieved[0]
                sideachieved = self.getside(cornerend,"LEFT")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="BR"):
                sideachieved = self.getside(cornerstart,"TOP")
                matchside = sideachieved[0]
                sideachieved = self.getside(cornerend,"BOTTOM")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="TR"):
                sideachieved = self.getside(cornerstart,"LEFT")
                matchside = sideachieved[0]
                sideachieved = self.getside(cornerend,"RIGHT")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            
            #the piece to be matched is corner start and the row vector contains the answer for each cycle
            piecematch = cornerstart
            rowvector = []
            while(not complete):
                # possible matchs are none right now
                possibleMatch = []
                for k in range(0, len(border)):
                    borderpiece = border[k]
                    for l in range(0, len(borderpiece.side)):
                        sideMatch = borderpiece.side[l]
                        if((not sideMatch.isStraight) and ((matchside.isConvex and sideMatch.isConcave) or (matchside.isConcave and sideMatch.isConvex)) and not piecematch == borderpiece):
                            # if the l side in k border can be a match check for its length and axis
                            canMatch = self.canmatchAngle(matchside,sideMatch)
                            # also check if we are matching the right border with the right corner or not
                            if(cornerstart.name == "TL" and not self.getside(borderpiece,"LEFT")[0].isStraight):
                                canMatch = False
                            if(cornerstart.name == "BL" and not self.getside(borderpiece,"BOTTOM")[0].isStraight):
                                canMatch = False
                            if(cornerstart.name == "BR" and not self.getside(borderpiece,"RIGHT")[0].isStraight):
                                canMatch = False
                            if(cornerstart.name == "TR"and not self.getside(borderpiece,"TOP")[0].isStraight):
                                canMatch = False
                            if(canMatch):
                                # if canMatch is true then add the piece to possible matches
                                possibleMatch.append([borderpiece,l])

                # check if the piece has the possiblity of matching the end corner
                canMatch=False
                if((not endmatchside.isStraight) and ((matchside.isConvex and endmatchside.isConcave) or (matchside.isConcave and endmatchside.isConvex))):
                    canMatch = self.canmatchAngle(matchside,endmatchside)
                if(canMatch):
                    possibleMatch.append([cornerend,endsidei])
                if(len(possibleMatch) == 0):
                    
                    return ["FAILED"]
                if(len(possibleMatch) == 1):
                    # if their is only one possible match then add it in rowvector 
                    rowvector.append([piecematch,matchside.direction,possibleMatch[0][0],possibleMatch[0][0].side[possibleMatch[0][1]].direction])
                    #set the next piece to be match
                    piecematch = possibleMatch[0][0]

                    # checking if the cycle need to be changed
                    if(cornerstart.name == "TL"):  
                        matchside = self.getside(piecematch,"BOTTOM")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BL"):
                        matchside = self.getside(piecematch,"RIGHT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)

                    elif(cornerstart.name == "BR"):
                        matchside = self.getside(piecematch,"TOP")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)

                    elif(cornerstart.name == "TR"):
                        matchside = self.getside(piecematch,"LEFT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)
                else:
                    # if the possibleMatch has more than one piece
                    for i in range(0,len(possibleMatch)):
                        startpos = []
                        endpos = []
                        # getting the start and end point for calculating the distance of the graph
                        startside1 = None
                        startside2 = None
                        if(len(matchside.sampleptreverse) < len(possibleMatch[i][0].side[possibleMatch[i][1]].samplept)):
                            startpos = matchside.sampleptreverse
                            endpos = possibleMatch[i][0].side[possibleMatch[i][1]].samplept
    
                        else:
                            endpos = matchside.sampleptreverse
                            startpos = possibleMatch[i][0].side[possibleMatch[i][1]].samplept
                        # getting the length of the graph
                        lena = matchside.lengthofside
                        lenb = possibleMatch[i][0].side[possibleMatch[i][1]].lengthofside
                        maxlen = max(lena,lenb)
                        minlen = min(lena,lenb)
                        startc = []    
                        endc = []
                        if(len(matchside.colourreverse) < len(possibleMatch[i][0].side[possibleMatch[i][1]].colour)):
                            startc = matchside.colourreverse
                            endc = possibleMatch[i][0].side[possibleMatch[i][1]].colour
                        else:
                            endc = matchside.colourreverse
                            startc = possibleMatch[i][0].side[possibleMatch[i][1]].colour
                        Coldis = self.colourintotal(startc,endc)
                        # calculting the different in the graph of the two and adding the difference in the length of the graph
                        # length is also used since the perfect match will have min(maxlen-minlen) and min(self.disintotal(startpos,endpos))
                        distance =  self.disintotal(startpos,endpos) +(maxlen-minlen)    
                        distance = 0
                        if(useColor and not useShape):
                            distance = (maxlen-minlen)+Coldis
                        elif(useShape and not useColor):
                            distance =  self.disintotal(startpos,endpos) +(maxlen-minlen)
                        else:
                            distance =  self.disintotal(startpos,endpos) +(maxlen-minlen)+Coldis





                        disis = self.disintotal(startpos,endpos)
                        distance =  disis +(maxlen-minlen)+Coldis
                        possibleMatch[i].append(distance)
                        possibleMatch[i].append(disis)
                        possibleMatch[i].append(Coldis)
                        possibleMatch[i].append((maxlen-minlen))
                        if(disis >=1500):
                            possibleMatch[i].append("F")
                        else:
                            possibleMatch[i].append("T")





                        # append the distance with the possiblematch piece
                    # gets the piece with smallest distance 
                    # meaning this is the piece to be matched
                    match = self.smallerdistance(possibleMatch)
                    # adding it to the rowvector
                    rowvector.append([piecematch,matchside.direction,match[0],match[0].side[match[1]].direction])

                    #set the next piece to be match
                    piecematch = match[0]
                    # checking if the cycle need to be changed
                    if(cornerstart.name == "TL"):  
                        matchside = self.getside(piecematch,"BOTTOM")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BL"):
                        matchside = self.getside(piecematch,"RIGHT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BR"):
                        matchside = self.getside(piecematch,"TOP")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "TR"):
                        matchside = self.getside(piecematch,"LEFT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

        resultvector = []
        resultvector.append([matchvector[0][0][0]])
        # addint the result of matchvector in resultvector
        # resultvector is 2D array which will contain the piece
        # in order meaning that if a piece is on the lowwer right most then 
        # it should be display on the lowwer right most
        '''
        resultvector = [
            row 0            [piece1, piece2, piece3, piece4, piece5, ....]
            row 1            [piece1, piece2, piece3, piece4, piece5, ....]
            row 2            [piece1, piece2, piece3, piece4, piece5, ....]
            row 3            [piece1, piece2, piece3, piece4, piece5, ....]
                             ....
                       ]
        '''
        # adding the first column
        for i in range(0,len(matchvector[0])):
            resultvector.append([matchvector[0][i][2]])
        # adding the first row
        for i in range(len(matchvector[3])-1,-1,-1):
            resultvector[0].append(matchvector[3][i][0])
        #adding the last row
        for i in range(0,len(matchvector[1])):
            resultvector[len(resultvector)-1].append(matchvector[1][i][2])
        # finding the match for the center pieces
        for dv in range(1,len(resultvector)-1):
            # this for loop finds the match for each row

            #the pieces to be matched is the first piece of the dv row
            matchpiece = resultvector[dv][0]
            # the side to be matched is right
            matchside = self.getside(matchpiece,"RIGHT")[0]
            for k in range(0,len(resultvector[0])-2):
                #matchpiece.showImage("PIECE to be matched")
                #finds the match for each piece in the row (column of result vector)
                # the top pieces is recieved since it could be use to get more accurate results
                toppiece = resultvector[dv-1][k+1]
                possiblepiece = []

                for i in range(0,len(center)):
                    centerpieces = center[i]
                    for j in range(0,len(centerpieces.side)):
                        sideMatch = centerpieces.side[j]
                        if(not sideMatch.isStraight and ((matchside.isConvex and sideMatch.isConcave) or (matchside.isConcave and sideMatch.isConvex))):
                            '''
                                if the j side of i center piece and that piece could be a possible match then
                                check if it matchs the matchpiece and it should also match the toppiece
                            '''
                            canMatch = self.canmatchAngle(matchside,sideMatch)
                            canMatchtop = self.canmatchAngle(self.getside(toppiece,"BOTTOM")[0],self.getside(centerpieces,"TOP")[0])
                            if(canMatch and canMatchtop):
                                # if it matchs both of the pieces then add it in possiblepiece
                                possiblepiece.append([i,j])
                
                if(len(possibleMatch) == 0):
                    return ["FAILED"]
                if(len(possiblepiece)==1):
                    # if their is only one possible match then add it in resultvector 
                    # and move to the next piece 
                    resultvector[dv].append(center[possiblepiece[0][0]])
                    matchpiece = center[possiblepiece[0][0]]
                    matchside = self.getside(center[possiblepiece[0][0]],"RIGHT")[0]
                    # removing the matched piece to reduce complexity for next piece
                    center.pop(possiblepiece[0][0])
                    #matchpiece.showImage("MATCHED only 1")
                    
                else:
                    for j in range(0,len(possiblepiece)):
                        possibleMatchm = center[possiblepiece[j][0]]
                        startpos = []
                        endpos = []

                        topsideA = self.getside(possibleMatchm,"TOP")[0]
                        bottomsideA = self.getside(toppiece,"BOTTOM")[0]
                        # getting the start and end point for calculating the distance of the graph

                        if(len(matchside.sampleptreverse) < len(center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept)):
                            startpos = matchside.sampleptreverse
                            endpos = center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept
            
                        else:
                            endpos = matchside.sampleptreverse
                            startpos = center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept
                        

                        if(len(matchside.colourreverse) < len(center[possiblepiece[j][0]].side[possiblepiece[j][1]].colour)):
                            startc = matchside.colourreverse
                            endc = center[possiblepiece[j][0]].side[possiblepiece[j][1]].colour
                        else:
                            endc = matchside.colourreverse
                            startc = center[possiblepiece[j][0]].side[possiblepiece[j][1]].colour
                        graphaColorDiffer = self.colourintotal(startc,endc)

                        # calculting the different in the graph of the two 
                        graphaDistance =  self.disintotal(startpos,endpos)  
                        #distance =  self.disintotal(startpos,endpos)  + Coldis

                        # getting the start and end point for calculating the distance of the graph
                        if(len(topsideA.sampleptreverse) < len(bottomsideA.samplept)):
                            startpos = topsideA.sampleptreverse
                            endpos = bottomsideA.samplept
            
                        else:
                            endpos = topsideA.sampleptreverse
                            startpos = bottomsideA.samplept

                        
                        if(len(topsideA.colourreverse) < len(bottomsideA.colour)):
                            startc = topsideA.colourreverse
                            endc = bottomsideA.colour
                        else:
                            endc = topsideA.colourreverse
                            startc = bottomsideA.colour
                        graphbColorDiffer = self.colourintotal(startc,endc)

                        # adding the distance between two graph since the match has to have the minimum 
                        graphbDistance =   self.disintotal(startpos,endpos)
                        
                        distance = 0
                        if(useColor and not useShape):
                            distance = graphaColorDiffer + graphbColorDiffer
                        elif(useShape and not useColor):
                            distance =  graphaDistance+graphbDistance
                        else:
                            distance =  graphaDistance+graphbDistance + graphaColorDiffer + graphbColorDiffer

                        # adding the distance to the possiblepiece
                        possiblepiece[j].append(distance)

                    #getting the piece wîth the smallest distance
                    match = self.smallerdistance(possiblepiece)
                    # adding the matched piece to the resultvector and moving to the next piece
                    resultvector[dv].append(center[match[0]])
                    matchpiece = center[match[0]]
                    #matchpiece.showImage("MATCHED")
                    matchside = self.getside(center[match[0]],"RIGHT")[0]
                    # removing the matched piece to reduce complexity for next piece
                    center.pop(match[0])
        # adding the last column in the resultvector from the macthvector 
        k = 1
        for i in range(len(matchvector[2])-1,0,-1):
            resultvector[k].append(matchvector[2][i][0])
            k =k +1 
        return ["COMPLETE",self.showresult(resultvector), resultvector]

    """
        copyes the given image to the target
        the starting location of the image is at x,y in traget
    """
    def imcopy(self,image,target,pieces,x=0,y=0):
        height, width, channels = target.shape 
        height2, width2, channels2 = image.shape 
        tmpim= image
        dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
        #convertinf it into grayscale image
        gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        #making the threshold of the grayscaled image
        ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        #dectecting the contours of the pieces    
        im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        var=contoursPi[0]
        intensities = []



        cimg = np.zeros_like(tmpim)
        cv2.drawContours(cimg, contoursPi, 0, color=255, thickness=-1)

            # Access the image pixels and create a 1D numpy array then add to list
        pts = np.where(cimg == 255)
        lst_intensities=[]
        lst_intensities.append(tmpim[pts[0], pts[1]])
        newpoints = []
        for i in range(0,len(pts[0])):
            newpoints.append([pts[1][i],pts[0][i]])
        pts = newpoints
        for i in range(0,len(pts)):
                newx = pts[i][1]+int(x)
                newy = pts[i][0]+int(y)
                
                colo = lst_intensities[0][i]
                target[newx][newy]  = colo
    """
        returns the width and height of the image 
    """
    def getWidthAndHeight(self,row,column):
        '''
            extra width and height given to the window
        '''
        width = 40
        height = 40
        for i in range(0,len(row)):
            piece = row[i]
            side = self.getside(piece,"TOP")[0]
            width = width + self.getDistance(side.cornerRight,side.cornerLeft)

        for i in range(0,len(column)):
            piece = row[i]
            side = self.getside(piece,"LEFT")[0]
            height = height + self.getDistance(side.cornerRight,side.cornerLeft)
        return [int(height),int(width)]
    """
        returns the image containg the result
    """
    def showresult(self,resultvector):
        height,width = self.getWidthAndHeight(resultvector[0], [row[0] for row in resultvector])
        newImageAppro = np.zeros((height,width,3), np.uint8)  
        for i in range(0,height):
            for j in range(0,width):
                newImageAppro[i][j] = [255,255,255]
        Oheight = 0
        xHeight = [0]*len(resultvector[0])
        Owidth = 0
        for i in range(0,len(resultvector)):
            Owidth=0
            for j in range(0,len(resultvector[i])):
                Oheight2 = xHeight[j]
                if (not i== 0):
                    resultimage = resultvector[i-1][j].image
                    height, width, channels = resultimage.shape 
                    leftside = self.getside(resultvector[i-1][j],"LEFT")[0]
                    minpoint = leftside.getmaxcornerpoint()
                    extra1 = round(self.getDistance([minpoint[0],height],minpoint)) 

                    leftside = self.getside(resultvector[i][j],"LEFT")[0]
                    minpoint = leftside.getmincornerpoint()
                    extra = round(self.getDistance([minpoint[0],0],minpoint)) 
                    xHeight[j] = xHeight[j]-extra -extra1

                resultimage = resultvector[i][j].image
                height, width, channels = resultimage.shape 
                topside = self.getside(resultvector[i][j],"TOP")[0]
                if(not j == 0):
                    minpoint = topside.getmincornerpoint()
                    extra = round(self.getDistance([0,minpoint[1]],minpoint) )
                    Owidth = Owidth -extra
                    
                self.imcopy(resultimage,newImageAppro,resultvector[i][j],y= Owidth,x=xHeight[j])
    
                minpoint = topside.getmaxcornerpoint()
                extra = round(self.getDistance([width,minpoint[1]],minpoint) )

                Owidth = Owidth + width -extra
                leftside = self.getside(resultvector[i-1][j],"LEFT")[0] 
                minpoint = leftside.getmaxcornerpoint()
                extra1 = round(self.getDistance([minpoint[0],height],minpoint)) 
                xHeight[j] = int(xHeight[j])+int(height)
        return newImageAppro

    """
        returns the smallest distance object in possibleoutcome
    """
    def smallerdistance(self,possibleoutcome):
        
        smallindex = 0
        smallDis = 900000000 #assuming the first element is the smallest
        for i in range(0,len(possibleoutcome)):
            if(possibleoutcome[i][2] < possibleoutcome[smallindex][2] and not possibleoutcome[i][len(possibleoutcome[i])-1] == "F"):
                smallindex = i
        return possibleoutcome[smallindex]

        
    """
        calculates the difference of the two graph  sent
    """
    def disintotal(self,grapha,graphb):
        finaldis = 0
        #goes in the first graph
        for i in range(0,len(grapha)):
            x1 = grapha[i][0]
            y1 = grapha[i][1]
            distance = []
            #goes for 10 different points in the second graph and uses the 
            #smaller distance among them
            for j in range(i-6,i+6):
                if(j>=0 and j < len(graphb)):
                    x2 = graphb[j][0]
                    y2 = graphb[j][1]
                    x = (x1-x2)**2   
                    y = (y1-y2)**2
                    dis = (x + y)**(0.5)
                    distance.append([dis,j])
            smalldis = [distance[0][0],distance[0][1]]
            for j in range(0,len(distance)):
                if(distance[j][0]<smalldis[0]):
                    smalldis = distance[j]
            finaldis = finaldis + smalldis[0]
        return finaldis



    """
        calculates the difference of colour in two graph  sent
    """
    def colourintotal(self,grapha,graphb):
        finaldis = 0
        #goes in the first graph
        for i in range(0,len(grapha)):
            b1 = grapha[i][0]
            g1 = grapha[i][1]
            r1 = grapha[i][2]
            
            distance = []
            #goes for 10 different points in the second graph and uses the 
            #smaller distance among them
            for j in range(i-5,i+6):
                if(j>=0 and j < len(graphb)):

                    
                    b2 = graphb[i][0]
                    g2 = graphb[i][1]
                    r2 = graphb[i][2]
                    
# Red Color
                    color1_rgb = sRGBColor(r1/255, g1/255, b1/255);
# Blue Color
                    color2_rgb = sRGBColor(r2/255, g2/255, b2/255);
# Convert from RGB to Lab Color Space
                    color1_lab = convert_color(color1_rgb, LabColor);
    # Convert from RGB to Lab Color Space
                    color2_lab = convert_color(color2_rgb, LabColor);
# Find the color difference
                    delta_e = delta_e_cie2000(color1_lab, color2_lab);
                    db = math.fabs(b2-b1)
                    dg =math.fabs(g2-g1)
                    dr = math.fabs(r2-r1)
                    pctb = db/255
                    pctg = dg/255
                    pctr = dr/255
                    #d=((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)**0.5
                    d = (pctb + pctg +pctr)/3
                    distance.append([delta_e,j])
            smalldis = [distance[0][0],distance[0][1]]
            for j in range(0,len(distance)):
                if(distance[j][0]<smalldis[0]):
                    smalldis = distance[j]
            finaldis = finaldis + smalldis[0]
        return finaldis        

        
        
                    
                
            
      
                
            
