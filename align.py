#First select the vertices, then the curve

import maya.cmds as cmds

#window size
winID = 'alignVtx'
WIDTH = 300
HEIGHT = 180


if cmds.window(winID, ex=True):
    cmds.deleteUI(winID)
    
#init window
cmds.window(winID, title='Snap Vertices', wh=(WIDTH,HEIGHT), mxb=False, toolbox=True)

col = cmds.columnLayout(adjustableColumn=True, rs=10)
boxRow = cmds.rowLayout(parent=col, nc=3)
boxX = cmds.checkBox(parent=boxRow, label='Move X', value=False)
boxY = cmds.checkBox(parent=boxRow, label='Move Y', value=False)
boxZ = cmds.checkBox(parent=boxRow, label='Move Z', value=False)

#numberOfRadioButtons = nrb, vertical=vr, select=sl
sortOpt = cmds.radioButtonGrp(parent=col, label='Sort in', numberOfRadioButtons=3, vertical=True, la3=['X', 'Y', 'Z'], select=1)

#reverse sort order
revButton = cmds.checkBox(parent=col, label='Reverse', value=False)

cmds.button(parent=col, label='Move', command='distrMain()')

cmds.showWindow()
cmds.window(winID, e=True, wh=(WIDTH,HEIGHT))

#Entry point
def distrMain():
    sel = cmds.ls(sl=True, fl=True)
    moveX = cmds.checkBox(boxX, q=True, v=True)
    moveY = cmds.checkBox(boxY, q=True, v=True)
    moveZ = cmds.checkBox(boxZ, q=True, v=True)
    sortAxis = cmds.radioButtonGrp(sortOpt, q=True, sl=True)

    # last item must be curve
    lastItem = sel[-1]
    if cmds.objectType(lastItem, isType='transform'):
        if cmds.objectType(cmds.listRelatives(lastItem, s=True)[0], isType='nurbsCurve'):
            AlignVer(sortVerts(sel[:-1], sortAxis-1), sel[-1], [moveX, moveY, moveZ])  
    else:
        cmds.error('Error: Last selction must be a NURB curve')
        #distrLine(sortVerts(sel, sortAxis-1), (moveX,moveY,moveZ))

#Distribute along curve        
def AlignVer(verts, crv, axes=[False, False, False]):
    numPositions = len(verts) - 1
    for i in range(len(verts)):
        #top=turnOnPercentage
        coord = cmds.pointOnCurve(crv, top=True, pr=float(i)/float(numPositions))
        
        print(coord[1])
        print(cmds.pointPosition(verts[i], w=True))
        cmds.move(coord[0], coord[1], coord[2], verts[i], absolute=True, x=axes[0], y=axes[1], z=axes[2], worldSpace=True)
        print(cmds.pointPosition(verts[i], w=True))


#Sort the vertices based on either their X, Y, or Z coordinates
def sortVerts(verts, axis):
    result = []
    for i in verts:
        result.append(i)
    result.sort(key=lambda vtx : cmds.pointPosition(vtx)[axis])
    if cmds.checkBox(revButton, q=True, v=True):
        result.reverse()
    return result
