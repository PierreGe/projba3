#!/usr/bin/python2
# -*- coding: utf8 -*-


import math, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL,GLU
import ObjParser


class OpenGLWidget(QtOpenGL.QGLWidget):
    # Public interface
    def __init__(self, object_names = [], parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.lightPosition = [-10,10,0]
        self.shadows = []
        self._object_names = object_names


    def getObjectNames(self):
        """ Reload openGLWidget """
        return self._object_names

    def setObjects(self, object_names):
        for obj in self.objects:
            GL.glDeleteLists(1, GL.GL_COMPILE)
        self._object_names = object_names
        self.loadObjects()


    # Rotation
    def xRotation(self):
        return self.xRot
 
    def yRotation(self):
        return self.yRot
 
    def zRotation(self):
        return self.zRot
 
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
 
    def sizeHint(self):
        return QtCore.QSize(400, 400)
 
    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()
 
    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()
 
    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()
 
    # Called at startup
    def initializeGL(self):
        # initial rotation
        self.xRot = 15
        self.yRot = -30
        self.zRot = 0
        self.zoom = -30

        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()

        # create some light sources FIX THAT SHIT
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION,  (-40, 200, 100, 0.0))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHTING)
        # save mouse cursor position for smooth rotation
        self.lastPos = QtCore.QPoint()
        # create floor and load .obj objects
        self.makeFloor()
        self.loadObjects()
        self.shadowVolume()

    # Objects construction methods
    def makeFloor(self):
        self.groundPoints = [-1,0,-1,-1,0,1,1,0,1,1,0,-1]
        self.groundList = GL.glGenLists(1)
        GL.glNewList(self.groundList, GL.GL_COMPILE)
        self.quadrilatere(*(([x*10 for x in self.groundPoints])))
        GL.glEndList()

    def loadObjects(self):
        self.objects = []
        for obj in self._object_names:
            item = ObjParser.ObjParser(obj[0])
            self.objects.append((item, obj[1]))
 
    # Called on each update/frame
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        # reload new matrix
        GL.glLoadIdentity()
        # zoom out camera
        GL.glTranslated(0, 0, self.zoom)
        # apply rotation
        GL.glRotated(self.xRot, 1, 0, 0)
        GL.glRotated(self.yRot, 0, 1, 0)
        GL.glRotated(self.zRot, 0, 0, 1)
        # paint objects
        self.paintFloor()
        self.paintObjects()

    def paintFloor(self):
        GL.glColor3f(1,1,1) # WHITE
        GL.glCallList(self.groundList)

    def paintObjects(self):
        GL.glColor3f(1,0,0) # RED
        for obj in self.objects:
            GL.glPushMatrix()
            GL.glTranslated(*obj[1])
            GL.glCallList(obj[0].gl_list)
            GL.glPopMatrix()

 
    # Called when window is resized
    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
 
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-10, 10, -10, 10, 1, 37) # FRUSTUUUUUUUUM ()
 
        GL.glMatrixMode(GL.GL_MODELVIEW)
 
    # Events
    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())
 
    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
 
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)
 
        self.lastPos = QtCore.QPoint(event.pos())
 
    def wheelEvent(self, event):
        self.zoom += event.delta()/100.0
        self.updateGL()
 
    # Work methods
    def quadrilatere(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4): 
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex3d(x1, y1, z1)
        GL.glVertex3d(x2, y2, z2)
        GL.glVertex3d(x3, y3, z3)
        GL.glVertex3d(x4, y4, z4)
        GL.glEnd()

    
    def getShapeOnGround(self):
        for point in self.objects[0][0].vertices:#for the vectrices composing the object n°0
            if point[1] < self.lightPosition[1]:#If light source is above the item, else no shadow on the ground
                from_light = [point[i]-self.lightPosition[i] for i in range(3)]#vector between light and item point

                norm = (from_light[0]**2 + from_light[1]**2 + from_light[2]**2)**(1/3.0)

                unit_vector = [from_light[i]/norm for i in range(len(from_light))]

                distance = (point[1])/unit_vector[1]
            self.shadows.append(point[0]-distance*unit_vector[0])
            self.shadows.append(point[1]-distance*unit_vector[1])
            self.shadows.append(point[2]-distance*unit_vector[2])
            #vecteur directeur de la droite light->point de la forme
        print self.shadows
        # self.shapeList = GL.glGenLists(10)
        # GL.glNewList(self.shapeList, GL.GL_COMPILE)
        # self.quadrilatere(*(([x*10 for x in self.shapeList])))
        # GL.glEndList()


        

    def shadowVolume(self):
        self.getShapeOnGround()
        # GL.glBegin(GL.GL_POINTS)
        # for i in range(len(self.shadows)/3):
        #     GL.glVertex3f(self.shadows[i], self.shadows[i+1], self.shadows[i+2])
        # GL.glEnd()





    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle
