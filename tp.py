import pandas as pd 
import scipy.signal as sig
import matplotlib.pyplot as plt 

def get_heartbeats(ecg):

    #Busco los picos de mayor importancia
    peak_index, _ = sig.find_peaks(ecg["señal"], prominence = 1)
    #Tomo los valores en los picos
    peaks = ecg["señal"].iloc[peak_index]
    #Tomo los tiempos en los que se produjeron los picos
    peak_times = ecg["tiempo"].iloc[peak_index]

    return peaks, peak_times

def get_status(frec, sex, age):

    max_m = 208.7 - 0.73*age
    max_f = 208.1 - 0.77*age

    if frec == 0:
        status = "El paciente está muerto\n"
    elif (frec > 0) and (frec < 60):
        status = "El paciente está durmiendo\n"
    else:
        if sex == 'M':
            if frec < max_m:
                status = "El paciente está haciendo ejercicio\n"
        elif sex == 'F':
            if frec < max_f:
                status = "El paciente está haciendo ejercicio\n"
        else:
            status = "Debe haber un error en las mediciones\n"

    return status            

def want_to_save():
    ans = input("Desea guardar esta información? [y/n]\n")
    if ans == 'y':
        name = input("Ingrese el nombre deseado para el archivo:\n")
        return name
    elif ans == 'n':
        return None
    else:
        return want_to_save()


def save_status(frec, status, name):
    txt_name = name+".txt"
    status_frec = "La frecuencia cardíaca es de " + str(frec) + " pulsaciones por minuto\n"
    data = [status_frec, status]
    with open(txt_name, 'w') as txt:
        txt.writelines(data)

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

peaks, peak_times = get_heartbeats(ecg)

#Calculo la frec con una regla de 3 tomando la cantidad de picos producidos en el tiempo en que se tienen los datos
frec = int(60*len(peaks)/ecg["tiempo"].iloc[-1])
print("La frecuencia cardíaca es de", frec, "pulsaciones por minuto")

status = get_status(frec, sex, age)
print(status)

txt_name = want_to_save()
if txt_name is not None:
    save_status(frec, status, txt_name)

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

