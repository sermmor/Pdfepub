#!/usr/bin/env python
# -*- coding: utf-8 -*

import controladorEditaYFormatea
import sys
from PyQt4 import QtCore, QtGui, uic


app = QtGui.QApplication(sys.argv)
myWindow = controladorEditaYFormatea.ControladorEdita(None)
myWindow.show()
app.exec_()
