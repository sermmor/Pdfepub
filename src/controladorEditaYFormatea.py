#!/usr/bin/env python
# -*- coding: utf-8 -*

import modeloFormatea
import modeloLeePdf
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 

FormularioEdita = uic.loadUiType("vistaEditaFormatea.ui")[0] # Carga la IU

class ControladorEdita(QtGui.QMainWindow, FormularioEdita):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Manejadores eventos.
		self.pBtArchivoOrigen.clicked.connect(self.lanzarExaminarOrigen)
		self.pBtArchivoGuardar.clicked.connect(self.lanzarExaminarGuardar)
		self.pBtAnyadirTabu.clicked.connect(self.anyadeTabuALista)
		self.pBtEliminarTabu.clicked.connect(self.eliminaTabuDeLista)

		self.btAnyadirTexto.clicked.connect(self.anyadirTextoPDF)
		self.btBuscaReemplaza.clicked.connect(self.buscaYReemplaza)

		self.pBtTransformar.clicked.connect(self.lanzarTransformar)

	# Diálogo para la ruta origen.
	def lanzarExaminarOrigen(self):
		sPath = QtGui.QFileDialog.getOpenFileName(self, 'Open file...', '/home', "PDF files (*.pdf)")
		self.lEArchivoOrigen.setText(sPath)

	# Diálogo para la ruta destino.
	def lanzarExaminarGuardar(self):
		# Muestro la carpeta en la que está el fichero de origen, sino está seleccionada uso el '\home'.
		sPath = '/home' if (str(self.lEArchivoOrigen.text().toUtf8() == "")) else ("/").join(str(self.lEArchivoOrigen.text().toUtf8()).split("/")[:-1])
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

	# Añade texto desde un PDF a la caja de texto pTETextoPDF.
	def anyadirTextoPDF(self):
		sPathOrigen = str(self.lEArchivoOrigen.text().toUtf8())
		iInicioPagina = self.sBPagDesde.value()
		iFinPagina = self.sBPagHasta.value()

		if ((sPathOrigen != "") and (iInicioPagina <= iFinPagina)):
			# Leemos el texto.
			sTexto = modeloLeePdf.copiarPaginasDesdePdf(iInicioPagina, iFinPagina, sPathOrigen)
			# Pego el texto en la caja de texto pTETextoPDF junto con un salto de línea al final.
			self.pTETextoPDF.appendPlainText(sTexto.decode('utf-8'))
			self.pTETextoPDF.appendPlainText("\n")

	def buscaYReemplaza(self):
		sTextoBusca = str(self.lEBuscaEnTexto.text().toUtf8())
		sTextoReemplaza = str(self.lEReemplazaEnTexto.text().toUtf8())
		# Reemplaza lo selecionada sólo si la cadena es igual a la del campo de buscar (sTextoBusca).
		sTextoSelecionado = str(self.pTETextoPDF.textCursor().selectedText().toUtf8()) # Extraigo el texto seleccionado.
		if sTextoSelecionado.lower() == sTextoBusca.lower():
			# Reemplazar lo seleccionado por lo que haya en el campo sTextoReemplaza.
			self.pTETextoPDF.textCursor().insertText(sTextoReemplaza.decode('utf-8'))

		# Busca el texto y si lo encuentra lo selecciona.
		cursor = self.pTETextoPDF.find(sTextoBusca.decode('utf-8'))
		self.pTETextoPDF.setTextCursor(cursor)


	# Lanza la transformación a txt.
	def lanzarTransformar(self):
		sTexto = str(self.pTETextoPDF.document().toPlainText().toUtf8()) # Si no se pone el toUtf8() peta fijo, pero fijo.
		sPathDestino = str(self.lEArchivoGuardar.text().toUtf8())
		# Extraigo todas las palabras tabu de lWPalabrasTabu
		lFrasesTabu = []
		if (self.lWPalabrasTabu.count() > 0):
			for i in range(self.lWPalabrasTabu.count()):
				lFrasesTabu.append(str(self.lWPalabrasTabu.item(i).text().toUtf8()))
		
		if ((sTexto != "") and (sPathDestino != "")):
			# Lanzamos el modelo, que es el que formatea y guarda.
			modeloFormatea.formateaTextoYGuardaEnFichero(sTexto, lFrasesTabu, sPathDestino)

			# Como ha acabado de convertir el texto, lanzamos un mensaje de que ha acabado la conversión.
			msgBox 	= QMessageBox(QMessageBox.Information, u"Transformation finished",
			      u"Text saved in selected path.")
			msgBox.show()
			msgBox.exec_()

