#!/usr/bin/env python
# -*- coding: utf-8 -*

import modeloFormatea
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

formularioFormatea = uic.loadUiType("vistaFormatea.ui")[0] # Carga la IU

class ControladorFormatea(QtGui.QMainWindow, formularioFormatea):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Manejadores eventos.
		self.pBtArchivoOrigen.clicked.connect(self.lanzarExaminarOrigen)
		self.pBtArchivoGuardar.clicked.connect(self.lanzarExaminarGuardar)
		self.pBtAnyadirTabu.clicked.connect(self.anyadeTabuALista)
		self.pBtEliminarTabu.clicked.connect(self.eliminaTabuDeLista)

		self.pBtTransformar.clicked.connect(self.lanzarTransformar)

	# Diálogo para la ruta origen.
	def lanzarExaminarOrigen(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', '/home')
		self.lEArchivoOrigen.setText(sPath)

	# Diálogo para la ruta destino.
	def lanzarExaminarGuardar(self):
		# Muestro la carpeta en la que está el fichero de origen, sino está seleccionada uso el '\home'.
		sPath = '/home' if (str(self.lEArchivoOrigen.text()) == "") else ("/").join(str(self.lEArchivoOrigen.text()).split("/")[:-1])
		# Lanzo el diálogo con la carpeta elegida.
		sPath = QtGui.QFileDialog.getSaveFileName(self, 'Save in...', sPath)
		self.lEArchivoGuardar.setText(sPath)

	# Añade una frase en lEPalabraTabu a la lista de frases tabu.
	def anyadeTabuALista(self):
		qsFraseTabu = self.lEPalabraTabu.text() # La lista no añade cadenas, debe ser un objeto QString.
		self.lWPalabrasTabu.addItem(qsFraseTabu)
		self.lEPalabraTabu.setText("")


	# Elimina la primera frase seleccionada de la lista de frases tabu.
	def eliminaTabuDeLista(self):
		self.lWPalabrasTabu.takeItem(self.lWPalabrasTabu.currentRow())

	# Lanza la transformación a txt.
	def lanzarTransformar(self):
		sPathOrigen = str(self.lEArchivoOrigen.text())
		sPathDestino = str(self.lEArchivoGuardar.text())
		# Extraigo todas las palabras tabu de lWPalabrasTabu
		lFrasesTabu = []
		if (self.lWPalabrasTabu.count() > 0):
			for i in range(self.lWPalabrasTabu.count()):
				lFrasesTabu.append(str(self.lWPalabrasTabu.item(i).text()))
		
		if ((sPathOrigen != "") and (sPathDestino != "")):
			# Lanzamos el modelo, que es el que formatea y guarda.
			modeloFormatea.formateaFichero(sPathOrigen, lFrasesTabu, sPathDestino)

			# Como ha acabado de convertir el texto, lanzamos un mensaje de que ha acabado la conversión.
			msgBox 	= QMessageBox(QMessageBox.Information, u"Process finished",
			      u"Text saved in selected path.")
			msgBox.show()
			msgBox.exec_()



