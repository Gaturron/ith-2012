#!/usr/bin/python

import commands, sys, re

# Parametros globales para poder cambiar los difonos mas facil
diphones_dir = "difonos/difonosbase3/"
vowel = ['a', 'A']
consonant = ['k', 'l', 'm', 'p', 's']

# Chequea que el string pasado como parametro sea de la forma (CV)+
# Si da error nos avisa en que parte del string nos equivocamos
def checkPhonemes(input):

    # Funcion auxiliar para armar la exp. reg.
    def concatStr(list):
        string = ''
        for item in list: 
            string += str(item) 
        return string

    # Exp. regular del leguaje propuesto
    pattern = "(^((["+str(concatStr(consonant))+"])(["+str(concatStr(vowel))+"]))+$)"
    
    # Si coinicide seguimos, sino buscamos donde fallo
    if re.search(pattern, input):
        return True
    else: 
        for i in range(0, len(input)):
            if i % 2 == 0:
                if not(input[i] in consonant):
                    print 'Error procesando input: '+input[0:i+1]+' <---- se esperaba '+str(consonant)
                    return False
            else:
                if not(input[i] in vowel):
                    print 'Error procesando input: '+input[0:i+1]+' <---- se esperaba '+str(vowel)
                    return False

# Dado un string, te devuelve una lista con todos sus difonos
# Ej: 'kamala' => ['-k', 'ka', 'am', 'ma', 'al', 'la', 'a-']
def getDiphones(input):
    assert len(input) > 1, 'str debe ser mas largo'    
    
    res = ['-'+input[0]]
    for i in range(1, len(input)):
        res += [input[i-1]+input[i]]
    res += [input[len(input)-1]+'-']
    return res    

# Dado un string, genera otro con todos los comandos de praat para contacenar los difonos
def makePraatScript(input):
    # Obtenemos los difonos del input
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
    
    script = loadWavs + concatWavs
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
    print 'Mal pasaje de parametros: debe pasar el string de lo que quiere sintetizar'
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
            print 'Tomando los difonos de: ./'+diphones_dir

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
                print 'Archivo '+ input + '.wav creado con el archivo sintetizador'
            else:
                print 'Error ejecutando el script ' + input + '.praat, mensaje: ', status[1]     
