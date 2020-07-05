#Copyright (c) 2020 Hsu Cheng
#Email: Hsu.Cheng.GR@dartmouth.edu
#Inspired by https://www.youtube.com/watch?v=pynPZrSq3JU&t=173s

import maya.cmds as mc
import maya.mel as mm

import maya.OpenMayaUI as mui
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QSlider
import shiboken2

def showUI():
    
    try:
        mainWin.close()
    except:
        pass
    
    global mainWin
    mainWin = SnowUI()
    mainWin.show()


def getMayaWindow():
    """
    return the maya main window as a python object
    """
    ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)





def snowyObj():
    snowyFaces = mc.ls(sl=1)
    objName = snowyFaces[0].split(".")[0]
    faceNum = mc.polyEvaluate(objName, f=True)
    
    mc.duplicate(objName)
    
    mc.polyChipOff(snowyFaces[:], dup=True, kft=True, ch=True)
    mc.delete(objName + ".f[:" + str(faceNum-1) + "]")
    
   # create emmiter from surface
    emitter = mc.emitter( objName, n=objName + "_emitter" , typ = "surface",  r=5000, sro=0, nuv=0, cye='none', cyi=1, spd=0, srn=0, nsp=1, tsp=0, mxd=0, mnd=0, dx=1, dy=0, dz=0, sp=0)
    particle = mc.nParticle( n = objName + "_nParticles" )
    mc.connectDynamic( particle, em = emitter)
    
    NucleusList = mc.ls(type='nucleus')
    mc.setAttr(NucleusList[0] + ".gravity", 0)
    
    #parameter setting
    global snowParticleShape
    snowParticleShape = objName + "_nParticlesShape"
    
    mc.setAttr(objName + "_nParticlesShape" + '.dynamicsWeight', 0)
    mc.setAttr(objName + "_nParticlesShape" + '.conserve', 0)
    mc.setAttr(objName + "_nParticlesShape" + '.radius', 0.1)
    mc.setAttr(objName + "_nParticlesShape" + '.radiusScaleRandomize', 0.5)
    mc.setAttr(objName + "_nParticlesShape" + '.particleRenderType', 3)
    
    mc.setAttr(objName + "_nParticlesShape" + '.blobbyRadiusScale', 1.8)
    mc.setAttr(objName + "_nParticlesShape" + '.meshTriangleSize', 0.2)
    # set to quad shape
    mc.setAttr(objName + "_nParticlesShape" + '.meshMethod', 3)
    #smoothing snow polygon
    mc.setAttr(objName + "_nParticlesShape" + '.meshSmoothingIterations', 8)
    

    mc.select(objName + "_nParticles", r=True)
    snowPolygon = mm.eval("particleToPoly")


class SnowUI(QtWidgets.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(SnowUI, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        
    
        self.setWindowTitle('SnowUI')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.createLayout()
        self.createConnection()

        
    def createLayout(self):
        self.snowBtn = QtWidgets.QPushButton("Create Snow")
        
        #threshold 0~2
        self.title_1 = QLabel("threshold")
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(10)
        self.sl.setMaximum(30)
        self.sl.setValue(12)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(10)
        
        self.label = QLabel("0.1")
        self.label.setFont(QtGui.QFont("Sanserif", 10))
        
        self.sl.valueChanged.connect(self.changeThreshold)
        
        #blobby radius 0~20
        self.title_2 = QLabel("blobby radius")
        self.s2 = QSlider(Qt.Horizontal)
        self.s2.setMinimum(0)
        self.s2.setMaximum(200)
        self.s2.setValue(1.8)
        self.s2.setTickPosition(QSlider.TicksBelow)
        self.s2.setTickInterval(400)
        
        self.label2 = QLabel("1.8")
        self.label2.setFont(QtGui.QFont("Sanserif", 10))
        
        self.s2.valueChanged.connect(self.changeRadius)
        

        #mesh triangle size 0~10
        self.title_3 = QLabel("triangle size")
        self.s3 = QSlider(Qt.Horizontal)
        self.s3.setMinimum(0)
        self.s3.setMaximum(100)
        self.s3.setValue(0.2)
        self.s3.setTickPosition(QSlider.TicksBelow)
        self.s3.setTickInterval(100)
        
        self.label3 = QLabel("0.2")
        self.label3.setFont(QtGui.QFont("Sanserif", 10))
        
        self.s3.valueChanged.connect(self.changeSize)
        
        
        mainLayout = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()

        hbox.addWidget(self.snowBtn, 0, 0)
        mainLayout.addLayout(hbox)
        #mainLayout.setSpacing(8)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.title_1, 1, 0)
        hbox.addWidget(self.sl, 2, 0)
        hbox.addWidget(self.label, 2, 1)
        mainLayout.addLayout(hbox)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.title_2, 1, 0)
        hbox.addWidget(self.s2, 2, 0)
        hbox.addWidget(self.label2, 2, 1)
        mainLayout.addLayout(hbox)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.title_3, 1, 0)
        hbox.addWidget(self.s3, 2, 0)
        hbox.addWidget(self.label3, 2, 1)
        mainLayout.addLayout(hbox)
        
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)
        
        
    def createConnection(self):
        self.snowBtn.clicked.connect(self.makeSnowObj)
        
    def makeSnowObj(self):
        snowyObj()
        
    def changeThreshold(self):
        self.threshold = float((self.sl.value() - 10) / 20.0)
        self.label.setText(str(self.threshold))
        mc.setAttr(snowParticleShape + '.threshold', self.threshold)
        
    def changeRadius(self):
        self.radius = float(self.s2.value()/ 10.0)
        self.label2.setText(str(self.radius))
        mc.setAttr(snowParticleShape + '.blobbyRadiusScale', self.radius)
        
    def changeSize(self):
        self.size = float(self.s3.value()/ 10.0)
        self.label3.setText(str(self.size))
        mc.setAttr(snowParticleShape + '.meshTriangleSize', self.size)

if __name__ == '__main__':
    showUI()