#!/usr/bin/env python
# -*- coding: utf-8 -*

import modeloCreaEpub
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

formularioCreaEpub = uic.loadUiType("vistaCreaEpub.ui")[0] # Carga la IU

class ControladorCreaEpub(QtGui.QMainWindow, formularioCreaEpub):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Variable con el último path.
		self.lastPath = "/home"
		
		# Manejadores eventos.
		self.pBPortada.clicked.connect(self.lanzarExaminarPortada)
		self.pBDedicatoria.clicked.connect(self.lanzarExaminarDedicatoria)

		self.pBAnadirCita.clicked.connect(self.lanzarExaminarCita)
		self.pBBorrarCita.clicked.connect(self.lanzarBorrarCita)
		self.pBAnadirCapitulo.clicked.connect(self.lanzarExaminarCapitulo)
		self.pBBorrarCapitulo.clicked.connect(self.lanzarBorrarCapitulo)

		self.pBCrearEpub.clicked.connect(self.lanzarCreaEpub)

	def actualizarPath(self, sNuevoPath):
		# Elimino del sNuevoPath el fichero del final y asigno el path resultante a self.lastPath
		self.lastPath = "/home" if (str(sNuevoPath.toUtf8()) == "") else ("/").join(str(sNuevoPath.toUtf8()).split("/")[:-1])

	# Diálogo para la ruta portada.
	def lanzarExaminarPortada(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', self.lastPath, "JPG files (*.jpg)")
		if sPath != "":
			self.lEPortada.setText(sPath)
			self.actualizarPath(sPath)

	def lanzarExaminarDedicatoria(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', self.lastPath)
		if sPath != "":
			self.lEDedicatoria.setText(sPath)
			self.actualizarPath(sPath)

	def lanzarExaminarCita(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', self.lastPath)
		if sPath != "":
			self.lWCita.addItem(sPath)
			self.actualizarPath(sPath)

	def lanzarBorrarCita(self):
		self.lWCita.takeItem(self.lWCita.currentRow())

	def lanzarExaminarCapitulo(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', self.lastPath)
		if sPath != "":
			self.lWCapitulo.addItem(sPath)
			self.actualizarPath(sPath)

	def lanzarBorrarCapitulo(self):
		self.lWCapitulo.takeItem(self.lWCapitulo.currentRow())

	def extraerDesdeListWidget(self, lWidget):
		ret = []
		if (lWidget.count() > 0):
			for i in range(lWidget.count()):
				ret.append(str(lWidget.item(i).text().toUtf8()))
		return ret

	def lanzarCreaEpub(self):
		sPath = QtGui.QFileDialog.getSaveFileName(self, 'Save in...', self.lastPath)
		if sPath != "":
			self.actualizarPath(sPath)
			# Extraigo los datos y luego compruebo de que no haya datos vacíos.
			sTitulo = str(self.lETitulo.text().toUtf8())
			sAutor = str(self.lEAutor.text().toUtf8())
			pathPortadaImg = str(self.lEPortada.text().toUtf8())
			lPathDedicatorias = str(self.lEDedicatoria.text().toUtf8())
			if lPathDedicatorias == "":
				lPathDedicatorias = []
			else:
				lPathDedicatorias = [lPathDedicatorias]
			lPathCitas = self.extraerDesdeListWidget(self.lWCita)
			lPathCapitulos = self.extraerDesdeListWidget(self.lWCapitulo)

			# Lanzo la función de crear epub del modelo.
			modeloCreaEpub.createEpub(pathPortadaImg, lPathDedicatorias, lPathCitas, lPathCapitulos, str(sPath.toUtf8()), sTitulo, sAutor)

			# Lanzo mensaje de confirmación (epub creado en la ubicación indicada).
			msgBox 	= QMessageBox(QMessageBox.Information, u"Epub created",
			      u"Epub saved in selected path.")
			msgBox.show()
			msgBox.exec_()

