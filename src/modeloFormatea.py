#!/usr/bin/env python
# -*- coding: utf-8 -*

# Devuelve si acaba en ".".
def acabaEnPunto(frase):
    return (frase[-1] == ".")

def vorazColocaPuntoYAparte(sTexto):
    # Suele pasar que ".\n" es un punto y aparte. No siempre, pero es una muy buena manera de no pasar tardes poniendo asteriscos (HABEMUS 
    #algoritmo avido con probabilidad de error).
    #-> CONDICIÓN: número máximo caracteres en las 50 primeras líneas = número máximo de caracteres. Si la línea no supera este máximo menos 
    #4 y acaba en ".", reemplazar ".\n" por "*\n", estoy casi seguro que ni Calibre usa un heuristico así. NO ES INFALIBRE, DE AHÍ LO DE "voraz"

    # 1 - calcular máximo caracteres en las primeras 50 líneas.
    iAInspeccionar = 50
    iMaxCaracteresXLinea = 0
    lTextoSplit = sTexto.split("\n")
    if len(lTextoSplit) < iAInspeccionar:
        iAInspeccionar = len(lTextoSplit) # Como hay menos de 50 lineas, se inspeccionan todas las del texto.

    for i in range(iAInspeccionar):
        iCandidato = len(lTextoSplit[i])
        if iCandidato > iMaxCaracteresXLinea:
            iMaxCaracteresXLinea = iCandidato

    # 2 - Resto a ese máximo el número que he puesto de rendondeo de fin de línea, que es 4.
    iMaxCaracteresXLinea = iMaxCaracteresXLinea - 4
    # 3 - Ahora que tenemos el máximo toca colocar los futuros punto y aparte (representados como "*\n").
    ret = ""
    for frase in lTextoSplit:
        # ¿Acaba en punto? ¿la longitud de la frase es menor que el máximo?
        iLenFrase = len(frase)
        if (iLenFrase > 0) and acabaEnPunto(frase) and (iLenFrase <= iMaxCaracteresXLinea):
            frase = frase + "*" # Como cumple la condición del ávido Añado el asterisco.
        ret = ret + frase + "\n"

    return ret


def formateaTexto(sTexto, lFrasesTabu):
    # Elimino frases de margenes.
    ret = sTexto
    for fraseTabu in lFrasesTabu:
        ret = ret.replace(fraseTabu + "\n", "")
    # Elimino números de página (máximo 1000).
    for i in range(1000):
        ret = ret.replace("\n" + str(i) + "\n", "\n") #Fijate que los números de página se identifican bien porque están solos en la línea.

    # Calcular dónde están los posibles puntos y aparte del texto (además de los ya marcados por el usuario con un asterisco).
    ret = vorazColocaPuntoYAparte(ret)

    #AQUÍ puedes añadir métodos para quitar el número de página o eliminar frases iniciales que salen en el margen superior de cada página.
    return ret.replace("-\n", "").replace("\n", " ").replace("* ", "\n")

def formateaFichero(sPathFicheroOrigen, lFrasesTabu, sPathFicheroDestino):
    # Leo fichero en sPathFicheroOrigen
    f = open(sPathFicheroOrigen, "Ur")
    sTexto = f.read()
    f.close()

    # Formateo
    formatText = formateaTexto(sTexto, lFrasesTabu)

    # Guardo el texto formateado en sPathFicheroDestino
    f = open(sPathFicheroDestino, "w")
    f.write(formatText)
    f.close()

def formateaTextoYGuardaEnFichero(sTexto, lFrasesTabu, sPathFicheroDestino):
    # Formateo
    formatText = formateaTexto(sTexto, lFrasesTabu)

    # Guardo el texto formateado en sPathFicheroDestino
    f = open(sPathFicheroDestino, "w")
    f.write(formatText)
    f.close()
    