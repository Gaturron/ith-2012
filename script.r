# Ejercicio 1
# Los hablantes de mayor edad suelen usar palabras de mayor longitud.
#gente <- read.table('test1.csv', sep=',', colClasses=c('character', 'character', 'character', 'integer', 'integer'), col.names=c('name','audio','sex', 'Edad', 'Cantidad.de.fonos'))
#age <- gente[,"Edad"]
#amount <- gente[,"Cantidad.de.fonos"]
#plot(age, amount)
#abline(lm(amount~age))
#cor.test(age, amount)
# La linea debe crecer de la punta izquierda abajo hasta la derecha arriba
# para que de correlacion deberia esta igual a la q mostramos
#boxplot(age)

# Ejercicio 2
# Los hombres producen pausas (silencios entre segmentos de habla) más cortas que las mujeres.
# version promedio
men <- read.table('test2-menProm.csv', sep=',',col.names=c('name', 'audio', 'sex', 'prom'))
promMen <-men[,'prom']
women <- read.table('test2-womenProm.csv', sep=',',col.names=c('name', 'audio', 'sex', 'prom'))
promWomen <-women[,'prom']
# Hipotesis a probar: muH < muM
# H0: muH > muM        H1: muH <= muM
t.test(promMen, promWomen, alternative='less')
# 	Welch Two Sample t-test

# data:  promMen and promWomen 
# t = 1.9707, df = 198.294, p-value = 0.9749
# alternative hypothesis: true difference in means is less than 0 
# 95 percent confidence interval:
#        -Inf 0.06032997 
# sample estimates:
# mean of x mean of y 
# 0.4984685 0.4656551 
# p-value no es menor que 0.05, entonce sno podems rechazar H0

# Hipotesis a probar: muH != muM
t.test(promMen, promWomen, alternative='two.sided')

# 	Welch Two Sample t-test

# data:  promMen and promWomen 
# t = 1.9707, df = 198.294, p-value = 0.05015
# alternative hypothesis: true difference in means is not equal to 0 
# 95 percent confidence interval:
#  -0.0000218982  0.0656486380 
# sample estimates:
# mean of x mean of y 
# 0.4984685 0.4656551 
# p-value entre 0.05 y 0.1 approaching significance... aprecen ser distintos 

# Hipotesis a probar: muH > muM
t.test(promMen, promWomen, alternative='greater')

# 	Welch Two Sample t-test

# data:  promMen and promWomen 
# t = 1.9707, df = 198.294, p-value = 0.02508
# alternative hypothesis: true difference in means is greater than 0 
# 95 percent confidence interval:
#  0.005296771         Inf 
# sample estimates:
# mean of x mean of y 
# 0.4984685 0.4656551 
# p-value 0.02 asique podemos rechazar Ho y afirmar que muH > muM
# o sea las mujeres producen pausas mas cortas que los hombres

# version todos los espacios
menPauses <- read.table('test2-menPauses.csv', sep=',')
womenPauses <- read.table('test2-womenPauses.csv', sep=',')
# Hipotesis a probar: muH > muM
t.test(menPauses, womenPauses, alternative='greater')
# 	Welch Two Sample t-test

# data:  menPauses and womenPauses 
# t = 3.1586, df = 2548.519, p-value = 0.000802
# alternative hypothesis: true difference in means is greater than 0 
# 95 percent confidence interval:
#  0.01539295        Inf 
# sample estimates:
# mean of x mean of y 
# 0.4930671 0.4609351 
# p-value 0.000082 podemos rechazar Ho y seguir afirmando que
# o sea las mujeres producen pausas mas cortas que los hombres

# Ver si se puede hacer boxplot de las pausas, pero creo que no
# allPausesProm <- append(as.data.frame(promWomen),as.data.frame(promMen))
# boxplot(allPausesProm)

# Ejercicio 3
# El habla espontánea tiene un tono de voz más grave que el habla leída. 
