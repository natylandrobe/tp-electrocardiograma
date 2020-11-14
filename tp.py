import pandas as pd 
import scipy.signal as sig
import matplotlib.pyplot as plt 

#Loop para preguntar la edad hasta que se ingrese una válida
while True:
    age = input("Por favor ingrese la edad del paciente en años:\n")
    if not age.isnumeric():
        print("Edad invalida")
        continue
    age = int(age)
    if(age < 0 or age > 150):
        print("Edad invalida")
        continue
    break

#Loop para preguntar el sexo hasta obtener uno válido
while True:
    sex = input("Por favor ingrese su sexo (M o F):\n")
    sex = sex.upper()
    if (sex != "M") and (sex != "F"):
        print("Sexo inválido")
        continue
    break

#Leer el archivo del ECG y guardarlo en un dataframe
ecg = pd.read_excel("https://raw.githubusercontent.com/IEEESBITBA/Curso-Python/master/Clase_4_datos/electrocardiograma.xlsx")

#Busco los picos de mayor importancia
peak_index, _ = sig.find_peaks(ecg["señal"], prominence = 1)
#Tomo los valores en los picos
peaks = ecg["señal"].iloc[peak_index]
#Tomo los tiempos en los que se produjeron los picos
peak_times = ecg["tiempo"].iloc[peak_index]

#Calculo la frec con una regla de 3 tomando la cantidad de picos producidos en el tiempo en que se tienen los datos
frec = int(60*len(peaks)/ecg["tiempo"].iloc[-1])

#Grafico
plt.plot(peak_times, peaks, 'go', label = "Picos")
plt.plot(ecg["tiempo"], ecg["señal"])
plt.title("ECG. Frecuencia = " + str(frec))
plt.xlabel("s")
plt.ylabel("eV")
plt.legend()
plt.grid(b = True, which = 'both')
plt.minorticks_on()
plt.grid(b = True, which = 'minor')
plt.show()