#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import math
from pieces import pieces
from result import Result 
# read the image throught an window frame 
#imports for that
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
from tkinter import messagebox
import tkinter as tk
from tkinter import *
import _thread
import threading
import warnings
import time
from PIL import Image
warnings.filterwarnings("ignore")


#from multiprocessing import Process
class constraintThread(threading.Thread):
    def __init__(self ,main):
        threading.Thread.__init__(self)
        self.startPoint = 0
        self.endPoint = len(main.jigsawpieces)
        self.jigsawPieces = main.jigsawpieces
        self.main = main
    
    """
        setPropertyOfPeces find the corner for each pieces in jigsaw puzzle
        and then sets the constrants for assembling the puzzle
    """

    def run(self):
        try:
            self.main.workingOnConstrats = True
            self.main.constraintBt.configure(bg="red")

            start_time = time.clock()
            for i in range(self.startPoint,self.endPoint):
                print(i)
                eachPiece = self.jigsawPieces[i]
                flag = eachPiece.findingcorners()
                if(flag == "CORNER_NOT_FOUND"):
                    messagebox.showerror("Error", "Error in reading the file")
                    break
                #setting the property of each side in the piece
                eachPiece.side[0].setsideproperty()
                eachPiece.side[1].setsideproperty()
                eachPiece.side[2].setsideproperty()
                eachPiece.side[3].setsideproperty()
                #setting the direction of the piece 
                eachPiece.setdirection()
                eachPiece.extractColour()
                if(time.clock() - start_time>=15):
                    start_time = time.clock()
                    print("Percentage completed -------- ",(i/len(self.main.jigsawpieces)*100))
            if(i+1 == self.endPoint):
                self.main.workingOnConstrats = False
                self.main.constraintBt.configure(bg=self.main.addBt.cget("bg"))
                self.main.solveBt.configure(bg=self.main.addBt.cget("bg"))
                self.main.constraintExtracted = True
                print("SETTING THE CONSTRAINTS DONE-----------------------------------")
            else:
                messagebox.showerror("Error", "Error in reading the file")
                self.main.errorInReading = True
                self.main.constraintBt.configure(bg=self.main.addBt.cget("bg"))
                self.main.workingOnConstrats = False
                print("SETTING THE CONSTRAINTS ERROR-----------------------------------")
        except:
                messagebox.showerror("Error", "Error in reading the file")
                self.main.errorInReading = True
                self.main.constraintBt.configure(bg=self.main.addBt.cget("bg"))
                self.main.workingOnConstrats = False
                print("SETTING THE CONSTRAINTS ERROR-----------------------------------")
            

class solvethread(threading.Thread):
    def __init__(self ,main):
        threading.Thread.__init__(self)
        self.main = main
        # making the object of result class and sending the pieces
        self.result = Result(main.jigsawpieces)
    def run(self):
		try:
            self.main.runningSolve = True
        
            result = self.result.getresult()
            if(result[0] == "MIX_PUZZLE"):
                messagebox.showwarning("Error", "There are more than one puzzle given")
                self.main.reset = True
                print("Solving THE Jigsaw Failed-----------------------------------")
            if(result[0] == "PIECE_MISSING"):
                messagebox.showwarning("Error", "Some of the pieces are missing")
                self.main.reset = True
                print("Solving THE Jigsaw Failed-----------------------------------")
            
            if(result[0] == "FAILED"):
                messagebox.showerror("Error", "The solver was unable to find the solution")
                self.main.reset = True
                print("Solving THE Jigsaw Failed-----------------------------------")
            
            if(result[0] == "COMPLETE"):
                success, self.main.resultimage , self.main.resultvector = result
                self.main.reset = False
                self.main.showrBt.configure(bg=self.main.addBt.cget("bg"))
                print("Solving THE Jigsaw Completed-----------------------------------")
                #shows the result
            self.main.runningSolve = False
		except:
			messagebox.showerror("Error", "The solver was unable to find the solution")
            self.main.reset = True
            print("Solving THE Jigsaw Failed-----------------------------------")
            self.main.runningSolve = False
			
            
        


class Main:
    """
        __init__ creates all the variable needed for the project
    """
    def __init__(self):
        self.win = None
        self.image =[]
        self.filename=None
        self.jigsawpieces = []
        self.resultimage = None
        self.resultvector = None
        self.labelImage = []
        self.logo = []
        self.workingOnConstrats = False
        self.constraintExtracted = False
        self.solveBt = None 
        self.addBt = None
        self.showrBt = None
        self.constraintBt = None
        self.reset = False
        self.errorInReading = False
        self.testing = False
        self.runningSolve = False
        self.errorInSolving = False
    """
        readFile reads the file from the directory and get the image
        then it disaplys on the screan which can be remove or open in a new image
    """
    def readFile(self):
        filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
        # addending all the images in an array
        if(filename == None or filename == ""):
            return False
        try:
            file = cv2.imread(filename)
            resized_image = cv2.resize(file, (400, 400)) 
            zoom = 10
            photo = PhotoImage(file=filename).subsample(zoom)
            while (photo.width()<=100):
                zoom = zoom-2
                photo = PhotoImage(file=filename).subsample(zoom)
            while (photo.width()>=200):
                zoom = zoom+2
                photo = PhotoImage(file=filename).subsample(zoom)
        except:
            messagebox.showerror("Error", "The Format of the file does is not supported")
            return False
        startposition = int(len(self.image)/4)+1
        endposition = int(len(self.image)%4)
        self.image.append(file)
        
        #displaying the image on the screen
        self.logo.append(photo)
        label = Button(self.win, image=self.logo[len(self.logo)-1])
        #Button-1 means right click
        #Button-3 means left click
        label.bind('<Button-1>',self.showImage)
        label.bind('<Button-3>', self.deleteImage)
        label.grid(row=startposition, column=endposition)
        self.labelImage.append(label)
        #updaing the windows
        self.win.update()
        return True
    """
        show the image which has been clicked
    """
    def showImage(self,event):  
        i = 0
        # getting which image is been clicked
        for i in range(0,len(self.labelImage)):
            if(event.widget == self.labelImage[i]):
                break
        cv2.imshow("Puzzle ",self.image[i])
    """
        delets the image which has been clicked
    """
    def deleteImage(self,event):  
        i = 0
        # getting which image is been clicked
        for i in range(0,len(self.labelImage)):
            if(event.widget == self.labelImage[i]):
                break
        self.labelImage[i].destroy()
        self.labelImage.pop(i)
        self.image.pop(i)

        # if the deleted image is the last one the resetting everthing
        # so the user can put a diferent image
        if(self.reset):

            self.jigsawpieces = []
            self.resultimage = None
            self.resultvector = None
            self.workingOnConstrats = False
            self.constraintExtracted = False
            self.solveBt.configure(bg ="red")
            self.showrBt.configure(bg ="red")
            self.errorInReading = False
            self.errorInSolving = False
            self.runningSolve = False

        if(len(self.labelImage)==0 and not self.reset):


            self.jigsawpieces = []
            self.filename=None
            self.resultimage = None
            self.resultvector = None
            self.workingOnConstrats = False
            self.constraintExtracted = False
            self.solveBt.configure(bg ="red")
            self.showrBt.configure(bg ="red")
            self.errorInReading = False
            self.errorInSolving = False
            self.runningSolve = False
    
        #updating the image
        self.win.update()
    """
        detect each piece in the i th image in the array of the images
        after detecting the piece it add it in the jigsawpiece object
    """
    def detectPieces(self,i):
        #getting the current image
        img = self.image[i]

        #converting the image into grayscale for thresholding the image
        imggry = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(imggry, 230, 255, cv2.THRESH_BINARY_INV)
        # using the opencv method to find the contours of the image
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # for extracting the pieces
        # we find the minimum points and the maximum points for and contour
        # and then extract it from the image 
        xlow = []
        xhigh = []
        ylow = []
        yhigh = []
        
        # loop in contour to find the pieces
        for cnt in range(0, len(contours)):
            # if the contour size is less than 500 we ignore it
            # since it is not a piece and a noise
            if(cv2.contourArea(contours[cnt])<=500) :
                continue
            point=contours[cnt]
            txlow = contours[cnt][0][0][0]
            tyhigh = contours[cnt][0][0][1]
            tylow = contours[cnt][0][0][1]
            txhigh = contours[cnt][0][0][0]
            for pt in point:
                if(txlow>pt[0][0]):
                    txlow = pt[0][0]
                if(tylow>pt[0][1]):
                    tylow = pt[0][1]
                if(txhigh<pt[0][0]):
                    txhigh = pt[0][0]
                if(tyhigh<pt[0][1]):
                    tyhigh = pt[0][1]
            if(txlow == txhigh or txhigh==tyhigh):
                continue
            xlow.append(txlow-2)
            xhigh.append(txhigh+2)
            ylow.append(tylow-2)
            yhigh.append(tyhigh+2)
        images = []
        jigsawPieces = []
        #extracting each piece from the image given in the system Part 1
        for i in range(0, len(ylow)):
            images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
            self.jigsawpieces.append(pieces(images[i]))
        #    self.jigsawpieces[i].showImage("Pieces "+str(i))
        #cv2.waitKey(0)


    """
        trys to solve the puzzle using b-tree method 
        it use solve aprroaches to decrease the complexity of the tree
        these approaches are 
    """
    def setConstarints(self):
        thread = constraintThread(self)
        thread.start()
        
    def getResult(self):
        # the result solve the puzzle if the constrants are extracted properly
        # it returns the result image and resultvector
        if(self.runningSolve):
            messagebox.showinfo("Information", "Solving is in process")
            return
        thread = solvethread(self)
        thread.start()
    """
        shows the assemble puzzle
    """
    def showResult(self):
        
        if(self.resultimage is None):
            return
        print("SHOWING THE RESULTS--------------------------------------------")
        im = Image.fromarray(self.resultimage)
        cv2.imshow("The Result is ",self.resultimage)
    """
        creates the window to add image and tell the application to
        solve the puzzle
    """
    def createwindow(self):
        self.win = Tk()
        self.win.title("jIgSAw PuZZlE")
        self.win.geometry("700x400")
        self.addBt  = Button(self.win, text="ADD IMAGE", command=self.addimage)
        self.addBt.grid(row=0, column=0)

        self.constraintBt = Button(self.win, text="Constraint", command=self.constraint)
        self.constraintBt.grid(row=0, column=1)


        self.solveBt  = Button(self.win, text="Solve", command=self.solve) 
        self.solveBt.configure(bg ="red")

        self.solveBt.grid(row=0, column=2)

        self.showrBt  = Button(self.win, text="Show Result", command=self.showResult) 
        self.showrBt.configure(bg ="red")
        self.showrBt.grid(row=0, column=3)
        self.win.mainloop()
    """
        adds the image to the solver
    """
    def addimage(self):
        success = self.readFile()
    """
        solves the puzzle if possible
    """
    def solve(self):
        if(self.errorInReading):
            messagebox.showerror("Error", "Failed To read the Data")
            return
        if(self.errorInSolving):
            messagebox.showerror("Error", "Failed To solve the Data")
        if(len(self.image) <= 0):
            messagebox.showerror("Error", "No Image of puzzle is Inputed")
            return
        if(self.resultimage is None):
            if(self.constraintExtracted):
                print("GETTING THE RESULTS--------------------------------------------")
                self.getResult()
            else:
                messagebox.showinfo("Information", "Constranints have not been extracted")
        else:
            self.showResult()

    def constraint(self):
        if(self.errorInReading):
            messagebox.showerror("Error", "Failed To read the Data")
            return
        if(self.errorInSolving):
            messagebox.showerror("Error", "Failed To solve the Data")
        if(len(self.image) <= 0):
            messagebox.showerror("Error", "No Image of puzzle is Inputed")
            return
        if(self.resultimage is None):
            if(self.constraintExtracted):
                return
            if(not self.workingOnConstrats):
                print("DETECTING PIECES-----------------------------------------------")
                for i in range(0,len(self.image)):
                    self.detectPieces(i)
                print("DETECTING PIECES DONE------------------------------------------")
                print("SETTING THE CONSTRAINTS----------------------------------------")
                self.setConstarints()
                
            else:
                messagebox.showinfo("Information", "Constraint is been extracted")
        else:
            self.showResult()
    """
        runs the code
    """
    def run(self):
        self.createwindow()
solver = Main()
solver.run()