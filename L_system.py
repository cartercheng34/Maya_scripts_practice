from pymel.all import *
import maya.cmds as mc
import random 
import math 
from maya.OpenMaya import MVector
from functools import partial
import maya.mel as mm

#a = L_Tree()

#a.drawBranch(0, 0, 0, 0, 0, 1, 0, 0.2, 15)

#shape = circle( nr=(0, 1, 0), c=(0, 0, 0), r=1)
#extrude (shape, et=0, d= (0, 1, 0), l= 10)



def TreeWindow():
    if mc.window('TreeGeneratorUI', exists=True):
		mc.deleteUI('TreeGeneratorUI')
    
    window = mc.window("TreeGeneratorUI", title='L System Tree', widthHeight=(200, 400), sizeable=0, minimizeButton=0, maximizeButton=0)
    mc.columnLayout()
    
    mc.text(label="Number of branches (2-15): ")
    branchesText= mc.intField( minValue=2, value=9, maxValue=15 )
    #branchNum = mc.intField(branchesText, query = True, value = True)

    
    mc.text(label="Branch Angle (0-90): ")
    angleText = mc.intField( minValue=0, value=35, maxValue=90 )
    #angle = mc.intField(angleText, query = True, value = True)
    
    mc.text(label="Angle Variance (0-50)")
    angleVarianceText = mc.intField( minValue=0, value=6, maxValue=50 )
    #angleVariance = mc.intField(angleVarianceText, query = True, value = True)
    
    mc.text(label="Length Decay (0-100): ")
    lengthFactorText = mc.intField( minValue=0, value=85, maxValue=100 )
    #lengthFactor = mc.intField(lengthFactorText, query = True, value = True)
    
    mc.text(label="Length Variance (0-100): ")
    lengthVarianceText = mc.intField( minValue=0, value=15, maxValue=100 )
    #lengthVariance = mc.intField(lengthVarianceText, query = True, value = True)
    
    mc.text(label="Radius Decay (0-100): ")
    radiusFactorText = mc.intField( minValue=0, value=90, maxValue=100 )
    #radiusFactor = mc.intField(radiusFactorText, query = True, value = True)
    
    mc.text(label="Radius Variance(0-100): ")
    radiusVarianceText = mc.intField( minValue=0, value=10, maxValue=100 )
    #radiusVariance = mc.intField(radiusVarianceText, query = True, value = True)
    
    mc.text(label="initial radius (0-2) ")
    initialRadiusText = mc.floatField( minValue=0, value=0.2, maxValue=2 )
    #initialRadius = mc.floatField(initialRadiusText, query = True, value = True)
    
    mc.text(label="initial length (0-100): ")
    initialLengthText = mc.intField( minValue=0, value=20, maxValue=100 )
    #initialLength = mc.intField(initialLengthText, query = True, value = True)
    
    mc.button(label="Draw Tree", command = lambda *args: drawTree(branchesText, angleText, angleVarianceText, lengthFactorText, lengthVarianceText, radiusFactorText, radiusVarianceText, initialRadiusText, initialLengthText), width=100, height=30)
    mc.button(label="Reset Parameter", command = lambda *args: Reset(branchesText, angleText, angleVarianceText, lengthFactorText, lengthVarianceText, radiusFactorText, radiusVarianceText, initialRadiusText, initialLengthText), width=100, height=30)

def Reset(branchesText, angleText, angleVarianceText, lengthFactorText, lengthVarianceText, radiusFactorText, radiusVarianceText, initialRadiusText, initialLengthText):
    
    #mm.eval("intField -edit -value 	9	branchesText;")
    win2 = TreeWindow()
    mc.showWindow(win2)


def drawTree(branchesText, angleText, angleVarianceText, lengthFactorText, lengthVarianceText, radiusFactorText, radiusVarianceText, initialRadiusText, initialLengthText):
    
    branchNum = mc.intField(branchesText, query = True, value = True)
    angle = mc.intField(angleText, query = True, value = True)
    angleVariance = mc.intField(angleVarianceText, query = True, value = True)
    lengthFactor = mc.intField(lengthFactorText, query = True, value = True)
    lengthVariance = mc.intField(lengthVarianceText, query = True, value = True)
    radiusFactor = mc.intField(radiusFactorText, query = True, value = True)
    radiusVariance = mc.intField(radiusVarianceText, query = True, value = True)
    initialRadius = mc.floatField(initialRadiusText, query = True, value = True)
    initialLength = mc.intField(initialLengthText, query = True, value = True)
    
    tree = L_Tree(branchNum, angle, angleVariance, lengthFactor, lengthVariance, radiusFactor, radiusVariance)
    

    tree.drawBranch(0, 0, 0, 0, 0, 1, 0, initialRadius, initialLength)
    
    

class L_Tree():
    def __init__(self, bran = 5, ang = 35, angleVar = 6, lengthFac = 85, lengthVar = 15, radiusFac = 90, radiusVar = 10):
        self.branches = bran
    	self.angle = ang
    	self.angleVariance = angleVar
    	self.lengthFactor = lengthFac/100.0
    	self.lengthVariance = lengthVar/100.0
    	self.radiusFactor = radiusFac/100.0
    	self.radiusVariance = radiusVar/100.0
    	
    	self.startingLength = 8
    	self.startingRadius = 1
    	
    	self.grp = mc.group( em=True)
    	print (self.grp)
    	

    def drawBranch(self, iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length):
    	if(iteration < self.branches):
    		iteration = iteration + 1
    		
    		#Draw circle and extrude based on parameters
    		shape = mc.circle( nr=(nrX, nrY, nrZ), c=(cX, cY, cZ), r=radius)
    		poly = mc.extrude (shape, et=0, d= (nrX, nrY, nrZ), l= length)
    		
    		mc.group( poly, parent = self.grp )
    		
    		#Delete the base circle and keep the cylinder
    		mc.delete(shape)
    		
    		#direction vector to grow
    		vector = MVector(nrX, nrY, nrZ)
    		vector.normalize()
    		
    		cX = cX + (length*vector.x)
    		cY = cY + (length*vector.y)
    		cZ = cZ + (length*vector.z)
    		
    		randX = r.randint(0, 1)*2 -1
    		randY = r.randint(0, 1)*2 -1
    		randZ = r.randint(0, 1)*2 -1
    		
    		#Random direction vector
    		#For X, Y, Z, ( -1 or 1 )*angle + (randint from -angleVariance to +angleVariance)
    		
    		nrX = nrX + ((self.angle*randX) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    		nrY = nrY + ((self.angle*randY) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    		nrZ = nrZ + ((self.angle*randZ) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    
    		#Length and Radius based on factor + (randint from -variance to +variance)
    		
    		length = length * (self.lengthFactor + (random.randint(0, self.lengthVariance*2*100)/100.0) - self.lengthVariance)
    		radius = radius * (self.radiusFactor + (random.randint(0, self.radiusVariance*2*100)/100.0) - self.radiusVariance)
    		
    		#Draw first branch
    		self.drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length)
    		
    		#Use opposite base angle from previous branch
    		
    		nrX = nrX + ((self.angle*randX*-1) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    		nrY = nrY + ((self.angle*randY*-1) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    		nrZ = nrZ + ((self.angle*randZ*-1) + random.randint(0, self.angleVariance*2) - self.angleVariance)/100.0
    
    		length = length * (self.lengthFactor + (random.randint(0, self.lengthVariance*2*100)/100.0) - self.lengthVariance)
    		radius = radius * (self.radiusFactor + (random.randint(0, self.radiusVariance*2*100)/100.0) - self.radiusVariance)
    		
    		#Draw second branch
    		self.drawBranch(iteration, cX, cY, cZ, nrX, nrY, nrZ, radius, length)
    		
if __name__ == '__main__':
    win = TreeWindow()
    mc.showWindow(win)
    		
    		