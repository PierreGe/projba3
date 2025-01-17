#!/usr/bin/python
# -*- coding: utf-8 -*-

from OpenGL.GL import *

import math
import threading

## ---- ###
LIGHT_POSSIBILITY = ["Point", "Directionnel", "Spot", "Ligne", "Rond"]
LIGHT_WITH_DIRECTION = ["Directionnel","Ligne","Spot"]
COLOR_POSSIBILITY = ["Blanc", "Rouge", "Jaune", "Bleu"]


class Light(object):
    """docstring for Light"""
    RATIO_DEGREE_RADIAN = 57.2957795
    def __init__(self):
        # interval pour eviter d'envoyer la lampe au perou
        self.lock = threading.Lock()
        self._xInterval = [-20,20]
        self._yInterval = [2,30]
        self._zInterval = [-20,20]

        xInit = (self._xInterval[1])
        yInit = (self._yInterval[1])
        zInit = (self._zInterval[1])

        self.setPosition([xInit, yInit, zInit])
        self._color = [1,1,1]
        self._type = "Point"

        self.modified = False

        self._verticalAngle = 45  # 0 vers le bas, 180 vers le plafond
        self._horizontalAngle = 0 # tourne sur lui meme

        self._theta = 0
        self._rayon = math.sqrt(self._xInterval[1]**2 + self._zInterval[1]**2) # warning  self._xInterval

    def resetLight(self):
        """ """
        self.__init__()

    def getPosition(self):
        return self._position

    def getIntensity(self):
        """ """
        return self._color

    def setPosition(self, position):
        "light with a custom position"
        self.lock.acquire()
        self._position = list(position)
        self.modified = True
        self.lock.release()


    def setIntensity(self, intensity):
        """ """
        self._color = intensity

    def getColor(self):
        """ """
        return self._color

    def setColor(self, color):
        """ """
        self._color = color

    def setModified(self, state):
        """ """
        self.modified = state

    def wasModified(self):
        """ """
        return self.modified

    def getType(self):
        """ """
        return self._type

    def setType(self, typed):
        """ """
        self._type = typed

    def setVerticalAngle(self,angle):
        """ """
        self._verticalAngle = angle
        self.modified = True

    def getVerticalAngle(self):
        """ """
        return self._verticalAngle 

    def setHorizontalAngle(self,angle):
        """ """
        self._horizontalAngle = angle

    def getHorizontalAngle(self):
        """ """
        return self._horizontalAngle 

    def getDirectionAsVec3f(self):
        """ """
        return (math.cos(self._horizontalAngle), math.sin(self._verticalAngle ), 1)


    def setLightsRatio(self,positionPercent):
        "light with a custom position"
        x = self._xInterval[0] + (float(positionPercent[0])/100 * ( abs(self._xInterval[0]) + abs(self._xInterval[1])))
        y = self._yInterval[0] + (float(positionPercent[1])/100 * ( abs(self._yInterval[0]) + abs(self._yInterval[1])))
        z = self._zInterval[0] + (float(positionPercent[2])/100 * ( abs(self._zInterval[0]) + abs(self._zInterval[1])))
        #print("{0}, {1}, {2}".format(x,y,z))
        self.setPosition([x,y,z])
        self.modified = True

    def setLightsRatioX(self,positionPercent):
        "light with a custom position"
        x = self._xInterval[0] + (float(positionPercent)/100 * ( abs(self._xInterval[0]) + abs(self._xInterval[1])))
        self._position[0] = x
        self.modified = True

    def setLightsRatioY(self,positionPercent):
        "light with a custom position"
        y = self._yInterval[0] + (float(positionPercent)/100 * ( abs(self._yInterval[0]) + abs(self._yInterval[1])))
        self._position[1] = y
        self.modified = True

    def setLightsRatioZ(self,positionPercent):
        "light with a custom position"
        z = self._zInterval[0] + (float(positionPercent)/100 * ( abs(self._zInterval[0]) + abs(self._zInterval[1])))
        self._position[2] = z
        self.modified = True

    def _normalizeAngle(self, angle):
        """ Keep the angle between 0 and 360"""
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle

    def setThetaAngle(self):
        """ """
        if self._position[0] < 0 and self._position[2] < 0:
            theta = math.atan(self._position[2]/self._position[0]) * Light.RATIO_DEGREE_RADIAN
            theta += 180
        elif self._position[2] > 0:
            theta = math.acos(self._position[0]/self._rayon) * Light.RATIO_DEGREE_RADIAN
        else:
            theta = math.asin(self._position[2]/self._rayon) * Light.RATIO_DEGREE_RADIAN

        self._theta = theta
        self.modified = True

    def incrementeRotate(self,plus):
        """ Increment Y value by plus, for rotation of the plane"""
        self.lock.acquire()
        self._theta +=  plus
        self._theta = self._normalizeAngle(self._theta)
        self._position[0] = self._rayon * math.cos(self._theta/Light.RATIO_DEGREE_RADIAN)
        self._position[2] = self._rayon * math.sin(self._theta/Light.RATIO_DEGREE_RADIAN)
        self.lock.release()


