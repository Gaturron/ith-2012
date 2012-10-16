#!/usr/bin/python

import sys
import commands

# Parametros globales para poder cambiar los difonos mas facil
vocal = ['a', 'A']
consonant = ['k', 'l', 'm', 'p', 's']
diphones_dir = "difonos/base1/"

# Chequea que el string pasado como parametro sea de la forma (CV)+
# Si da error nos avisa en que parte del string nos equivocamos
def checkPhonemes(input):
    for i in range(0, len(input)):
        if i % 2 == 0:
            if not(input[i] in consonant):
                print 'Error procesando input: '+input[0:i+1]+' <----'
                return False
        else:
            if not(input[i] in vocal):
                print 'Error procesando input: '+input[0:i+1]+' <----'
                return False
    return True

# Dado un string, te devuelve una lista con todos sus difonos
# Ej: 'kamala' => ['-k', 'ka', 'am', 'ma', 'al', 'la', 'a-']
def getDiphones(input):
    assert len(input) > 1, 'str debe ser mas largo'    
    
    res = []
    res.append('-'+input[0])
    for i in range(1, len(input)):
        res.append(input[i-1]+input[i])
    res.append(input[len(input)-1]+'-')   
    return res    

    #input2    = '-' + input + '-'
    #return [input2[i:i+2] for i in range(len(input2) - 1)]

# Dado un string, genera otro con todos los comandos de praat para contacenar los difonos
def makePraatScript(input):
    #obtenemos los difonos del input
    diphoneList = getDiphones(input)

    loadWavs = ''
    concatWavs  = ''
    count = 0
    for diphone in diphoneList:
        # Cargamos cada difono, lo renombramos y le decimos que se concatene
        loadWavs += 'Read from file... '+ diphones_dir + diphone + '.wav' + '\n'
        loadWavs += 'Rename... difono' + str(count) + '\n'  
        concatWavs += 'plus Sound difono' + str(count) + '\n'
        count += 1
    
    script = loadWavs 
    script += concatWavs
    script += 'Concatenate recoverably\n'
    script += 'select Sound chain\n'

    # Generamos el nuevo wav con el mismo nombre que el input
    script += 'Write to WAV file... ' + input + '.wav'
    return script

# Escribe el archivo .praat que va a ejecutar la concatenacion
def makePraatFile(input, script):
    praatFile = open(input + '.praat', 'w')
    praatFile.writelines(script)
    praatFile.close()

#Empieza el script
if len(sys.argv) < 2:
    print 'Mal pasaje de parametros: debe pasar el codigo en ascii de lo que quiere sintetizar'
else:
    input = sys.argv[1]

    if input == "--help":
        readme = open("LEEME.txt", "r")
        for line in readme.readlines():
            print line,
        readme.close()

    else:
        # Chequeamos que el input se pueda sintetizar
        if not checkPhonemes(input):
            print 'Mal los fonemas ingresados'
        else:
            print 'Sintetizando: '+input

            # Generamos los comandos para el script de Praat
            script = makePraatScript(input)
            
            print 'Generando script para Praat...',
            # Creamos el archivo
            makePraatFile(input, script)
            print 'OK'

            print 'Ejecutando el script en Praat...',
            status = commands.getstatusoutput('./praat ' + input + '.praat')
            
            if status[0] == 0:
                print 'Ok'
                print 'Archivo '+ input + '.wav creado con el archivo sintetizado'
            else:
                print 'Error ejecutando el script ' + input + '.praat, mensaje: ', status[1]     