#!/usr/bin/python

import sys
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

if len(sys.argv) < 2:
    print 'Mal pasaje de parametros: debe pasar el codigo en ascii de lo que quiere sintetizar'
else:
    string = sys.argv[1]
    print 'Parametro ingresado: '+string

    if not checkDiphones(string):
        print 'Mal los difonos ingresados'
    else:
        diphones = getDiphones(string)

        for i in range(0, len(diphones)):
            if i == 0:
                print 'select Sound '+diphones[0]
            else:
                print 'plus Sound '+diphones[i]
        print 'Concatenate recoverably'
