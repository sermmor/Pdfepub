#!/usr/bin/env python
# -*- coding: utf-8 -*

from ebooklib import epub

# Este fichero hace uso del fichero style.css para aplicar estilos.

def addMetadatos(book, sTitulo, sAutor):
	book.set_identifier('sample123456')
	book.set_title(sTitulo)
	book.add_author(sAutor)
	return book

def addCss(book):
	# Leo fichero style.css
	f = open("style.css", "Ur")
	sCss = f.read()
	f.close()
	# Añado el CSS.
	nav_css = epub.EpubItem(uid="style_nav", file_name="style/style.css", media_type="text/css", content=sCss)
	book.add_item(nav_css)

	return book, nav_css

def addCover(pathPortadaImg, book):
	book.set_cover("image.jpg", open(pathPortadaImg, 'r').read())
	return book

# Dado el número de la sección en Int, calcula el nombre de la sección en String.
def getNameSeccion(iNumeroSeccion):
	ret = "Section"
	# Averiguo el número de cifras de iNumeroSeccion. El truco está en ir haciendo modulo de potencia de 10 hasta que dé la misma cifra que iNumeroSeccion.
	iNumCifras = 1
	while (iNumeroSeccion%(10**iNumCifras) != iNumeroSeccion):
		iNumCifras = iNumCifras + 1

	# Son 4 los ceros entre "Section" y ".xhtml", hay que calcular cuántos ceros hacen falta.
	iNumCeros = 4 - iNumCifras

	# Añadir ceros.
	for i in range(iNumCeros):
		ret = ret + "0"

	# Añadimos a lo que tenemos el número de la sección pasado a cadena y la extensión del fichero.
	return ret + str(iNumeroSeccion) + ".xhtml"

# Devuelve en una cadena el contenido del capítulo.
def getContenidoCapitulo(sPathCapitulo, sNombreCapitulo, bIsDedicatoria, bIsCita):
	# Código html inicial para cada capítulo.
	sHtmlCodeIni = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title></title>
  <link href="../styles/style.css" rel="stylesheet" type="text/css" />
</head>

<body>
  '''
	# Código html entre el nombre del capítulo y el contenido del capítulo en sí.
	sHtmlCodeMiddle = "</h1>"
	# Código html que marca el final del capítulo.
	sHtmlCodeEnd = '''</body>
</html>'''
	

	# Extraigo lo que contiene el capítulo.
	f = open(sPathCapitulo, "Ur")
	sTexto = f.read()
	f.close()

	# Envolver cada párrafo entre <p> y </p>
	sTexto = ("\n").join(map((lambda sCadena: "<p>"+sCadena+"</p>"), sTexto.split("\n")))

	# Componemos el capítulo con su html.
	if sNombreCapitulo != "":
		sRet = sHtmlCodeIni + '''<h1>'''
		sRet = sRet + sNombreCapitulo.decode('utf-8')
		sRet = sRet + sHtmlCodeMiddle
	elif bIsDedicatoria:
		sRet = sHtmlCodeIni + '''<div class="dedicatoria"><i>'''
	elif bIsCita:
		sRet = sHtmlCodeIni + '''<div class="dedicatoria">'''
	else:
		sRet = sHtmlCodeIni

	sRet = sRet + sTexto.decode('utf-8')
	if bIsDedicatoria:
		sRet = sRet + '''</i></div>'''
	elif bIsCita:
		sRet = sRet + '''</div>'''
	sRet = sRet + sHtmlCodeEnd
	return sRet


def addChaptersYToc(lDedicatoriasYCitas, lPathCapitulos, book, defaultCss):
	# Extraigo nombre de cada capítulo (nombre del fichero)
	lNombreCapitulos = map((lambda cadena: cadena.split("/")[-1]), lPathCapitulos)
	
	# Añadir cada capítulo.
	lCapitulos = []
	iIndexCapitulo = 1
	for sPathCapitulo in lPathCapitulos:
		# Calculo nombre del archivo.
		sNombreArchivo = getNameSeccion(iIndexCapitulo)
		# Añado capítulo.
		c1 = epub.EpubHtml(title=lNombreCapitulos[iIndexCapitulo - 1].decode('utf-8'), file_name=sNombreArchivo)
		contenido = getContenidoCapitulo(sPathCapitulo, lNombreCapitulos[iIndexCapitulo - 1], False, False)
		c1.content = contenido.encode('utf-8')
		# Añado su css
		c1.add_item(defaultCss)
		# Añado el capítulo al libro.
		book.add_item(c1)

		# Añado capítulo a la lista.
		lCapitulos = lCapitulos + [c1]

		iIndexCapitulo = iIndexCapitulo + 1

	# Creamos el índice.
	book.toc = tuple(lCapitulos)
	# Añadimos ficheros de navegación.
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	# creamos spine, cover en la primera página, página de navegación, dedicatorias y citas y luego resto de capítulos.
	lCapitulos = ['cover', 'nav'] + lDedicatoriasYCitas + lCapitulos

	book.spine = lCapitulos

	return book

def addDedicatoriaYCitas(lPathDedicatorias, lPathCitas, book, defaultCss):
	lDedicatoriasYCitas = []
	i = 0
	for sPathDedicatoria in lPathDedicatorias:
		# Calculo nombre del archivo.
		sNombreArchivo = "dedicatoria" + str(i) + ".xhtml"
		# Añado capítulo.
		c1 = epub.EpubHtml(title="Dedicatoria", file_name=sNombreArchivo)
		contenido = getContenidoCapitulo(sPathDedicatoria, "", True, False)
		c1.content = contenido.encode('utf-8')
		# Añado su css
		c1.add_item(defaultCss)
		# Añado el capítulo al libro.
		book.add_item(c1)
		lDedicatoriasYCitas = lDedicatoriasYCitas + [c1]
		i = i + 1
	i = 0
	for sPathCita in lPathCitas:
		# Calculo nombre del archivo.
		sNombreArchivo = "cita" + str(i) + ".xhtml"
		# Añado capítulo.
		c1 = epub.EpubHtml(title="cita", file_name=sNombreArchivo)
		contenido = getContenidoCapitulo(sPathCita, "", False, True)
		c1.content = contenido.encode('utf-8')
		# Añado su css
		c1.add_item(defaultCss)
		# Añado el capítulo al libro.
		book.add_item(c1)
		lDedicatoriasYCitas = lDedicatoriasYCitas + [c1]
		i = i + 1
	return book, lDedicatoriasYCitas

# Método que dada una lista de path a txt (que pueden tener html dentro o no) con capítulos, crea un libro, con su indice. 
# Cada capítulo tendrá como título el nombre del fichero.
def createEpub(pathPortadaImg, lPathDedicatorias, lPathCitas, lPathCapitulos, pathGuardar, sTitulo, sAutor):
	book = epub.EpubBook()

	# Añado metadatos.
	book = addMetadatos(book, sTitulo, sAutor)
	# Crear portada.
	book = addCover(pathPortadaImg, book)
	# Añado el estilo (fichero "style.css" en el mismo path que este programa).
	book, defaultCss = addCss(book)
	# Añado dedicatorias y citas.
	book, lDedicatoriasYCitas = addDedicatoriaYCitas(lPathDedicatorias, lPathCitas, book, defaultCss)
	# Añado capítulos y crea indice.
	book = addChaptersYToc(lDedicatoriasYCitas, lPathCapitulos, book, defaultCss)
	# Guardamos todo el epub.
	epub.write_epub(pathGuardar, book, {})

