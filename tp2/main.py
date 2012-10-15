#!/usr/bin/python

import sys
import commands

vocal = ['a', 'A']
consonant = ['k', 'l', 'm', 'p', 's']

diphones_dir = "difonos/base1/"

def checkDiphones(input):
    for i in range(0, len(input)):
        if i % 2 == 0:
            if not(input[i] in consonant):
                print 'Mal input: '+input[0:i+1]
                return False
        else:
            if not(input[i] in vocal):
                print 'Mal input: '+input[0:i+1]
                return False
    return True

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

def makePraatScript(input):
    diphones = getDiphones(input)

    loadWavs = ''
    concatWavs  = ''
    soundCount = 0
    for each_diphone in diphones:
        loadWavs += 'Read from file... '+ diphones_dir + each_diphone + '.wav' + '\n'
        loadWavs += 'Rename... difono' + str(soundCount) + '\n'  
        concatWavs += 'plus Sound difono' + str(soundCount) + '\n'
        soundCount += 1
    
    script = loadWavs 
    script += concatWavs
    script += 'Concatenate recoverably\n'
    script += 'select Sound chain\n'
    script += 'Write to WAV file... ' + input + '.wav'
    
    return script

def makePraatFile(input, script):
    praatFile = open(input + '.praat', 'w')
    praatFile.writelines(script)
    praatFile.close()

#Empieza el script
if len(sys.argv) < 2:
    print 'Mal pasaje de parametros: debe pasar el codigo en ascii de lo que quiere sintetizar'
else:
    input = sys.argv[1]

    if input == "-help":
        print "Abirir el archivo LEEME"
    else:
        print 'Parametro ingresado: '+input

        if not checkDiphones(input):
            print 'Mal los difonos ingresados'
        else:
            print 'Sintetizando: '+input

            script = makePraatScript(input)
            
            print 'Generando script para praat...'
            makePraatFile(input, script)

            print 'Ejecutando praat...'
            status = commands.getstatusoutput('./praat ' + input + '.praat')
            
            if status[0] != 0:
                print 'Error al tratar de ejecutar el script, mensaje: ', status[1]
            else:
                print 'Ok'