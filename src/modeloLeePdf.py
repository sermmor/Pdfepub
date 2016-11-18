#!/usr/bin/env python
# -*- coding: utf-8 -*

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

# REQUISITO: ¡tener instalado pdfminer!
# Credits: http://stackoverflow.com/a/20905381 , y modificado del mismo para que acepte de entrada el lPageNumber.
def convert_pdf_to_txt(path, lPageNumber):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set(lPageNumber)
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

# Elimina espacios hasta 9 caracteres de largo.
def eliminaEspaciosLargos(sTxt):
	sRet = sTxt
	for i in range(19):
		sEspacio = (" ")*(i+2)
		sRet = sRet.replace(sEspacio, " ")
	return sRet

def eliminaLineasVacias(sTxt):
	sRet = sTxt
	# Si hay una línea en la que sólo hay un espacio, eliminar línea (para mayor efectividad antes de esto se debe haber ejecutado eliminaEspaciosLargos).
	sRet = sRet.replace("\n ", "")
	# Eliminamos todo dobles, triple,... hasta 20 enters seguidos.
	lrango = range(19)
	lrango.reverse()
	for i in lrango:
		sEnter = ("\n")*(i+2)
		sRet = sRet.replace(sEnter, "\n")

	return sRet

def eliminaEspaciosFinDeLinea(sTexto):
	return ("\n").join(sTexto.split(" \n"))

# Copia páginas desde un Pdf, elimina espacios largos y líneas vacías y devuelve el texto.
# Página inicio y fin ambas inclusives.
def copiarPaginasDesdePdf(iInicioPagina, iFinPagina, sPathFileEntrada):
	# Calculo lista de páginas a leer, basandome en las páginas inicio y fin dadas desde la entrada.
	lNumPaginas = range(iInicioPagina-1, iFinPagina)
	sTexto = convert_pdf_to_txt(sPathFileEntrada, lNumPaginas)
	# Elimina combinaciones de dobles, triples, cuadruples,... hasta 20 espacios transformándolos en uno solo.
	sTexto = eliminaEspaciosLargos(sTexto)
	# Elimina doble, triples,... hasta 20 enters seguidos transformándolos a uno solo.
	sTexto = eliminaLineasVacias(sTexto)
	# Eliminar las FF que indican el fin de una página en un pdf (en la tabla ASCII se corresponde con el decimal 12).
	sTexto = sTexto.replace(chr(12), "")
	# Eliminar espacios al final de cada línea.
	sTexto = eliminaEspaciosFinDeLinea(sTexto)
	return sTexto
