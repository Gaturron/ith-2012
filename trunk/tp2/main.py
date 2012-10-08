#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
vocal = ['a', 'A']
consonant = ['ḱ', 'l', 'm', 'p', 's']

def checkDiphones(str):
    for i in range(0, len(str)):
        if i % 2 == 0:
            if not(str[i] in consonant):
                print 'Mal input: '+str[0:i+1]
        if i % 2 == 1:
            if not(str[i] in vocal):
                print 'Mal input: '+str[0:i+1]

if len(sys.argv) < 2:
    print 'Mal pasaje de parametros: debe pasar el codigo en ascii de lo que quiere sintetizar'
else:
    str = sys.argv[1]
    print 'Parametro ingresado: '+str

    checkDiphones(str)
    