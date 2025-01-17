#!/usr/bin/python2
# -*- coding: utf8 -*-

import sys
import os
from PyQt4 import QtGui

class AlgoPanel(QtGui.QMainWindow):

    def __init__(self,controler):
        super(AlgoPanel, self).__init__()
        self._controler = controler
        self.initUI()
        
    def initUI(self):
        newAction = QtGui.QAction('Appliquer', self)
        newAction.setStatusTip('Applique les options')
        newAction.triggered.connect(self.send)

        
        menubar = self.menuBar()
        menubar.addAction(newAction)

        
        self.text = QtGui.QTextEdit(self)
        self.text.setText("""
            anti-aliasing-int : 4
            anti-aliasing-float : 4.0
            spreading : 700.0
            bias : 0.05""")
        
        self.setCentralWidget(self.text)
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Option des algorithme')
        self.show()
        
    def send(self):
        dico = {}
        string = str(self.text.toPlainText())
        list = string.split("\n")
        for line in list:
            try:
                key,value = line.split(":")
                dico[key.strip()] = value.strip()
            except:
                pass
        self._controler.setOption(dico)
        self.close()

        
def main():
    app = QtGui.QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
