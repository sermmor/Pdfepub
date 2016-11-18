#!/usr/bin/env python
# -*- coding: utf-8 -*

import controladorFormatea
import sys
from PyQt4 import QtCore, QtGui, uic


app = QtGui.QApplication(sys.argv)
myWindow = controladorFormatea.ControladorFormatea(None)
myWindow.show()
app.exec_()
