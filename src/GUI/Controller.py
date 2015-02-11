#!/usr/bin/python2
# -*- coding: utf8 -*-

import json
import io

from os import listdir
from os.path import isfile, join



import HelpWidget
import OpenGLWidget
import LightCollection

class Controller(object):
    """Controller will controll :
            - what widget is diplayed on the left part of the splitPane
            - what the statusBar show
        The controller also know all the scene"""
    def __init__(self):
        self._statusBar = None
        self._splitPane = None
        self._scene = {} # nom : obj-liste  (from assets/scene/)
        self._parseAllScene() #
        self._lightCollection = LightCollection.LightCollection()

        self._lightPosition = [0,0,0]
        self._glWidget = None
        self._helpWidget = HelpWidget.HelpWidget()

    def initStatusBar(self,statusBar):
        """ """
        self._statusBar = statusBar
        self._setStatusReady()

    def initSplitPane(self,splitPane):
        """ """
        self._setStatusComputing()
        self._splitPane = splitPane
        self._setStatusReady()

    def showGL(self, item):
        """ Set the right widget in the splitpane as the gl widget """
        self._setStatusComputing()

        scene = str(item.parent().text(0))
        algo = str(item.text(0))
        # TODO set algo
        self._glWidget = OpenGLWidget.OpenGLWidget(self._scene[scene]["obj-liste"],algo,self)
        self._replaceRightWidget(self._glWidget)

        self._setStatusReady()

    def showHelp(self):
        """ Set the right widget in the splitpane as help """
        self._setStatusComputing()

        self._replaceRightWidget(self._helpWidget)
        self._glWidget = None

        self._setStatusReady()

    def reload(self):
        """ """
        self._setStatusComputing()
        
        if self._glWidget:
            obj = self._glWidget.getObjectNames()
            algo = self._glWidget.getChosenAlgoName()
            self._glWidget = OpenGLWidget.OpenGLWidget(obj,algo,self)
            self._replaceRightWidget(self._glWidget)
        else:
            print("[WARNING] Unable to reload : no OpenGLWidget loaded!")
            QtGui.QMessageBox.error(self, "Erreur", "Unable to reload this OpenGl")

        self._setStatusReady()

    def addLight(self, light):
        """ """
        self._lightCollection.addLight(light)

    def deleteLight(self, light):
        """ """
        self._lightCollection.deleteLight(light)

    def getLightCollection(self):
        """ """
        return self._lightCollection

    def getAllScene(self):
        """ get the scene dictionnary"""
        return self._scene


    def lightPercentX(self,x):
        """ """
        self._lightPosition[0] = x
        self._updateLight()

    def lightPercentY(self,y):
        """ """
        self._lightPosition[1] = y
        self._updateLight()

    def lightPercentZ(self,z):
        """ """
        self._lightPosition[2] = z
        self._updateLight()

    def _updateLight(self):
        """ """
        if self._glWidget:
            self._glWidget.updateLights(self._lightPosition)

    def _parseAllScene(self):
        """ This method will assets/scene/ and add all the scene to a dictionnary"""
        mypath = "assets/scene/"
        scenesFiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        # remove auto-generated file : thanks macos!!!
        for singleFile in scenesFiles:
            if "json" in singleFile.lower():
                jasonDict = json.loads(open(mypath + singleFile).read())
                name = jasonDict["name"]
                dicti = jasonDict
                print(dicti["obj-liste"])
                if name in self._scene:
                    print("[WARNING] : Two scenes with same name found : the first one will be overwrited!")
                self._scene[name] = dicti

    def _replaceRightWidget(self,newWidget):
        """ replace the splitpane right widget"""
        self._splitPane.replaceRightWidget(newWidget)

    def _setStatusReady(self):
        """ set the statutus bar to ready"""
        self._statusBar.showMessage("Ready!")

    def _setStatusComputing(self):
        """ set the status bar to computing"""
        self._statusBar.showMessage("Computing ....")
