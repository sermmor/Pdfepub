#!/usr/bin/env python
# -*- coding: utf-8 -*

import controladorCreaEpub
import sys
from PyQt4 import QtCore, QtGui, uic


app = QtGui.QApplication(sys.argv)
myWindow = controladorCreaEpub.ControladorCreaEpub(None)
myWindow.show()
app.exec_()
