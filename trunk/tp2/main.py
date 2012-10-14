#!/usr/bin/python

import sys
import commands

vocal = ['a', 'A']
consonant = ['k', 'l', 'm', 'p', 's']

def checkDiphones(string):
    for i in range(0, len(string)):
        if i % 2 == 0:
            if not(string[i] in consonant):
                print 'Mal input: '+string[0:i+1]
                return False
        else:
            if not(string[i] in vocal):
                print 'Mal input: '+string[0:i+1]
                return False
    return True

def getDiphones(string):
    assert len(string) > 1, 'str debe ser mas largo'    
    
    res = []
    res.append('-'+string[0])
    for i in range(1, len(string)):
        res.append(string[i-1]+string[i])
    res.append(string[len(string)-1]+'-')   
    return res    

def makePraatScript(diphones, string):
    #se genera el script de praat
    praatReads = ''
    praatPlus  = ''
    script     = ''
    p1         = '-' + string + '-'
    #diphones  = [p1[i:i+2] for i in range(len(p1) - 1)]
    soundNames = 'difono'
    soundCount = 0
    for each_diphone in diphones:
        fName   = each_diphone + '.wav'
        praatReads += 'Read from file... difonos/base1/' + fName + '\n'
        praatReads += 'Rename... ' + soundNames + str(soundCount) + '\n'    #se renombra cada difono para que praat seleccione bien los objetos.
        praatPlus  += 'plus Sound ' + soundNames + str(soundCount) + '\n'
        soundCount += 1
    
    script += praatReads + praatPlus
    script += 'Concatenate recoverably\n'
    script += 'select Sound chain\n'
    script += 'Write to WAV file... ' + string + '.wav'
    
    return script

#Empieza el script
if len(sys.argv) < 2:
    print 'Mal pasaje de parametros: debe pasar el codigo en ascii de lo que quiere sintetizar'
else:
    string = sys.argv[1]
    print 'Parametro ingresado: '+string

    if not checkDiphones(string):
        print 'Mal los difonos ingresados'
    else:
        print 'Sintetizando: '+string
        diphones = getDiphones(string)

        scriptToRun = makePraatScript(diphones, string)
        
        print 'Generando script para praat...',
        scriptFile = open(string + '.praat', 'w')
        scriptFile.writelines(scriptToRun)
        scriptFile.close()
        print 'Ok'

        print 'Ejecutando praat...',
        status = commands.getstatusoutput('./praat ' + string + '.praat')
        
        if status[0] != 0:
            print 'Error al tratar de ejecutar el script, mensaje: ', status[1]
        else:
            print 'Ok'