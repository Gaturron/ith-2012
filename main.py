#!/usr/bin/python
# -*- coding: latin-1 -*-

import os, praat

ipuDir = "./ipus/"
wavDir = "./wavs/"

listaDatos = []

def getIpuData(fileName):
    file = open(fileName, 'r')
    lista = []
    for line in file:
        splittedLine = line.strip('\n').split(' ', 2)
        if len(splittedLine) > 2:
            lista.append([splittedLine[2], float(splittedLine[0]), float(splittedLine[1])])
    file.close()
    return lista

def getNumberPhones(filename): 
    data = getIpuData("./ipus/"+filename)
    phones = 0
    for item in data:
        if item[0] != '#':
            splittedLine = item[0].split(' ')
            #print splittedLine
            for word in splittedLine:
                phones = phones + len(word.strip().decode('utf-8', 'replace'))
                #print 'Cant phones: '+str(phones)
    return phones

#def writeCSV(IpuFiles, CSVname, function):
#    CSVfile = open(CSVname, 'w')
#    for file in IpuFiles:
#        name = file.split('.ipu')[0].split('-')
#        if len(name[1]) > 1 and (name[1])[1] == '1':
#            #poner todos los nombres con mayusculas
#            CSVfile.write(name[0]+' '+str(name[1])+' '+str(function(file))+'\n')
#    CSVfile.close()

def loadCSVData():
    file = open("data.csv",'r')
    global listaDatos
    for line in file:
        listaDatos.append(line.replace('"', "").split('\t'))
    file.close()
    file = open("datos.csv", 'r')
    for line in file:
        listaDatos.append(line.split(','))
    file.close()

    def sacaLugar(dato): 
        if len(dato) > 3:
            dato[0] = dato[0].title()
            return dato[0:4] 

    listaDatos = map(sacaLugar, listaDatos)

def getNumberPhonesList():
    list = [] #lista <name, phones>
    for fileName in os.listdir(ipuDir):
        if ".ipu" in fileName:
            nameList = fileName.split('.ipu')[0].split('-')

            if len(nameList) > 1:
                name = nameList[0]
                speaker = nameList[1]

                assert (len(speaker) > 1), 'Speaker debe ser A2 por ejemplo'
                if speaker[1] == '1':
                    list.append([name, speaker[0], getNumberPhones(fileName)])
    return list

#Mergea listaDatos con NumberPhonesList
def merge(DataList, PhonesList):
    merge = []
    for sp1 in DataList:
        for sp2 in PhonesList:
            if sp1[0].upper() == sp2[0].upper() and sp1[1] == sp2[1]:
                merge.append([sp1[0], sp1[1], sp1[2], sp1[3], sp2[2]]) 
    return sorted(merge)

def writeCSV(CSVname, list):
    CSVfile = open(CSVname, 'w')
    for item in list:
        
        assert (len(item) > 0), 'El item tiene que tener algo para grabar'

        if len(item) == 1:
            CSVfile.write(item[0]+'\n')
        else:
            for field in item:
                CSVfile.write(str(field))
                if item[-1] != field: #si no es el ultimo
                    CSVfile.write(', ')
            CSVfile.write('\n')
    CSVfile.close()

def writeCSV1(CSVname, list):
    CSVfile = open(CSVname, 'w')
    for item in list:
        CSVfile.write(str(item))
        CSVfile.write('\n')
    CSVfile.close()

#=========================================================================

def getSpeakers(): return listaDatos

def getGenreSpeakers(genre):
    assert (listaDatos != []), 'Antes se debe haber cargado el CSV de los hablantes'
    speakers = []
    for person in listaDatos:

        assert (len(person) > 3), 'Cada persona debe tener una lista con 3 elementos'

        if person[2].strip() == genre:
            speakers.append(person)
    return speakers
    
def getMenSpeakers(): return getGenreSpeakers('m')

def getWomenSpeakers(): return getGenreSpeakers('f')

def openIpu(speaker, audio): 
    for filename in os.listdir(ipuDir):
        if filename.title() == str(speaker[0])+"-"+str(speaker[1])+audio+".Ipu":
            #print "[+] "+str(speaker[0])+"-"+str(speaker[1])+audio+".ipu existe"    
            file = open("./ipus/"+filename,'r')
            lines = []
            for line in file:
                lines.append(line.strip('\n').split(' ', 2))
            file.close()
            return lines

    #print "[-] "+str(speaker[0])+"-"+str(speaker[1])+audio+".ipu no existe"
    return []

def averagePauseDuration(speaker, audio):
    ipu = openIpu(speaker, audio)
    if ipu != []:
        amount = 0
        duration = 0

        assert (len(ipu) > 2), 'Para que range no falle'

        for index in range(1, len(ipu)-1):
            if ipu[index-1][2] != '#' and ipu[index][2] == '#' and ipu[index+1][2] != '#':
                amount = amount+1
                duration = duration + (float(ipu[index][1]) - float(ipu[index][0]))
        assert (amount != 0), 'Sino div by zero'
        return duration / amount
    else:
        return -1

def averagePauseDurationForSpeakers(speakers):
    amount = 0
    duration = 0

    for speaker in speakers:
        for audio in ['1', '2']:
            ipu = openIpu(speaker, audio)
            if ipu != []:
                assert (len(ipu) > 2), 'Para que range no falle'

                for index in range(1, len(ipu)-1):
                    if (ipu[index-1][2] != '#') and (ipu[index][2] == '#') and (ipu[index+1][2] != '#'):
                        amount = amount + 1
                        duration = duration + (float(ipu[index][1]) - float(ipu[index][0]))
    assert (amount != 0), 'Sino div by zero'
    return duration / amount

def getPauses(speaker):
    pauses = []
    for audio in ['1', '2']:
        ipu = openIpu(speaker, audio)
        if ipu != []:
            assert (len(ipu) > 2), 'Para que range no falle'

            for index in range(1, len(ipu)-1):
                if (ipu[index-1][2] != '#') and (ipu[index][2] == '#') and (ipu[index+1][2] != '#'):
                    #print ipu[index]
                    duration = (float(ipu[index][1]) - float(ipu[index][0]))
                    pauses.append(duration)
    return pauses

def getPausesForSpeakers(speakers):
    list = []
    for speaker in speakers:
        list = list + getPauses(speaker)
    return list

def test2men():
    list = []
    for man in getMenSpeakers():
        avg = averagePauseDuration(man, '1')
        if(avg != -1): list.append([man[0], man[1]+'-1', 'm', str(avg)])
        
        avg = averagePauseDuration(man, '2')
        if(avg != -1): list.append([man[0], man[1]+'-2', 'm', str(avg)])
    return list

def test2women():
    list = []
    for woman in getWomenSpeakers():  
        avg = averagePauseDuration(woman,'1')
        if(avg != -1): list.append([woman[0], woman[1]+'-1', 'f', str(avg)])
        
        avg = averagePauseDuration(woman, '2')
        if(avg != -1): list.append([woman[0], woman[1]+'-2', 'f', str(avg)])
    return list

def test2a():
    list = []
    for man in getMenSpeakers():
        avg = averagePauseDuration(man, '1')
        if(avg != -1): list.append([man[0], man[1]+'-1', 'm', str(avg)])
        
        avg = averagePauseDuration(man, '2')
        if(avg != -1): list.append([man[0], man[1]+'-2', 'm', str(avg)])
        
    for woman in getMenSpeakers():  
        avg = averagePauseDuration(woman,'1')
        if(avg != -1): list.append([woman[0], woman[1]+'-1', 'f', str(avg)])
        
        avg = averagePauseDuration(woman, '2')
        if(avg != -1): list.append([woman[0], woman[1]+'-2', 'f', str(avg)])
    return list

#Los hombres producen pausas (silencios entre segmentos de habla) mas cortas que las mujeres.
def test2b():
    print 'Promedio hombres: '+str(averagePauseDurationForSpeakers(getMenSpeakers()))
    print 'Promedio mujeres: '+str(averagePauseDurationForSpeakers(getWomenSpeakers()))

#=========================================================================

def meanF0Total(speaker, audio):
    ipu = openIpu(speaker, audio)

    meanF0xSegTotal = 0
    durationTotal = 0
    if ipu != []:
        for line in ipu:
            
            assert ( len(line) > 2), 'line tiene que tener minimo 3 elementos'
            
            if line[2].strip() != "#":
            
                for filename in os.listdir(wavDir):
                    if filename.title() == str(speaker[0])+"-"+str(speaker[1])+audio+".Wav":

                        start = float(line[0])
                        end = float(line[1])
                        duration = end - start

                        #print wavDir+filename+" "+str(start)+" "+str(end) 
                        dicc = praat.run_praat(wavDir+filename, start, end, 75,500) 
                        meanF0Seg = dicc['f0_mean'] 
                        #print meanF0Seg

                        durationTotal = durationTotal + duration
                        meanF0xSeg = meanF0Seg * duration
                        meanF0xSegTotal = meanF0xSegTotal + meanF0xSeg

                        assert (durationTotal != 0), 'Sino div by zero'
                        return meanF0xSegTotal / durationTotal
                #print 'No hay audio '+str(speaker[0])
                return 0
    else:
        #print 'no hay ipu'
        return 0

def meanSimpleF0Total(speaker, audio):
    ipu = openIpu(speaker, audio)

    meanF0xSegTotal = 0
    SegTotal = 0
    if ipu != []:
        for line in ipu:
            
            assert ( len(line) > 2), 'line tiene que tener minimo 3 elementos'
            
            if line[2].strip() != "#":
            
                for filename in os.listdir(wavDir):
                    if filename.title() == str(speaker[0])+"-"+str(speaker[1])+audio+".Wav":

                        start = float(line[0])
                        end = float(line[1])
                        duration = end - start

                        #print wavDir+filename+" "+str(start)+" "+str(end) 
                        dicc = praat.run_praat(wavDir+filename, start, end, 75,500) 
                        meanF0Seg = dicc['f0_mean'] 
                        #print meanF0Seg

                        SegTotal = SegTotal + 1
                        meanF0xSegTotal = meanF0xSegTotal + meanF0Seg

                        assert (SegTotal != 0), 'Sino div by zero'
                        return meanF0xSegTotal / SegTotal
                #print 'No hay audio '+str(speaker[0])
                return 0
    else:
        #print 'no hay ipu'
        return 0

def meanF0SpontaneousSpeech():
    speakers = getSpeakers()
    
    meanF0 = 0
    amount = 0
    for speaker in speakers:
        if meanF0Total(speaker, '1') != 0:
            meanF0 = meanF0 + meanF0Total(speaker, '1')
            amount = amount + 1
    assert (amount != 0), 'Sino div by zero'
    return meanF0 / amount

def meanF0ReadSpeech():
    speakers = getSpeakers()
    
    meanF0 = 0
    amount = 0
    for speaker in speakers:
        if meanF0Total(speaker, '2') != 0:
            meanF0 = meanF0 + meanF0Total(speaker, '2')
            amount = amount + 1
    assert (amount != 0), 'Sino div by zero'
    return meanF0 / amount

def meansF0SpontaneousSpeech():
    speakers = getSpeakers()
    
    res = []
    for speaker in speakers:
        if meanF0Total(speaker, '1') > 0:
            res.append([speaker, meanF0Total(speaker, '1')])
    return res

def meansF0ReadSpeech():
    speakers = getSpeakers()
    
    res = []
    for speaker in speakers:
        if meanF0Total(speaker, '2') > 0:
            res.append([speaker, meanF0Total(speaker, '2')])
    return res


def meansSimpleF0SpontaneousSpeech():
    speakers = getSpeakers()
    
    res = []
    for speaker in speakers:
        if meanF0Total(speaker, '1') > 0:
            res.append([speaker, meanSimpleF0Total(speaker, '1')])
    return res

def meansSimpleF0ReadSpeech():
    speakers = getSpeakers()
    
    res = []
    for speaker in speakers:
        if meanF0Total(speaker, '2') > 0:
            res.append([speaker, meanSimpleF0Total(speaker, '2')])
    return res

#=========================================================================
loadCSVData()
#Test1: Los hablantes de mayor edad suelen usar palabras de mayor longitud.
#csv = merge(listaDatos, getNumberPhonesList())
#print csv
#writeCSV('test1.csv', csv)

#Test2: Los hombres producen pausas (silencios entre segmentos de habla) más cortas que las mujeres.
#promedio
#men = test2men()
#writeCSV('test2-menProm.csv', men)
#women = test2women()
#writeCSV('test2-womenProm.csv', women)

#todas las pausas
#menPauses = getPausesForSpeakers(getMenSpeakers())
#writeCSV1('test2-menPauses.csv', menPauses)
#womenPauses = getPausesForSpeakers(getWomenSpeakers())
#writeCSV1('test2-womenPauses.csv', womenPauses)

#Test3: El habla espontánea tiene un tono de voz más grave que el habla leída.
#Promedio ponderado para el calculo del tono de voz
# speaker, hablante
ss = meansF0SpontaneousSpeech()
print ss
lss=[]
for i in ss:
    lss.append(i[1])
writeCSV1('test3-meansF0SS.csv', lss)

rs = meansF0ReadSpeech()
print rs
lrs=[]
for i in rs:
    lrs.append(i[1])
writeCSV1('test3-meansF0RS.csv', lrs)
#Promedio simple a ver que pasa
ss1 = meansSimpleF0SpontaneousSpeech()
print ss1
lss1=[]
for i in ss1:
    lss1.append(i[1])
writeCSV1('test3-meansSimpleF0SS.csv', lss1)

rs1 = meansSimpleF0ReadSpeech()
print rs1
lrs1=[]
for i in rs1:
    lrs1.append(i[1])
writeCSV1('test3-meansSimpleF0RS.csv', lrs1)

print str(ss1 == ss)
