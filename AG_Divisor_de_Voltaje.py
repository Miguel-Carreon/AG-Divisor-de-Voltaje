import random
import math
import time

poblacion_inicial = []
poblacion_copy = []
poblacion_hijos = []
aptitud_lst = []
elite = []
inversion = []
rnum_1 = []
rnum_2 = []
r1 = []
r2 = []
iteraciones = 100 #En 100 iteraciones hay convergencia
iteracion = 0
vin = float(input('Inserte el valor del voltaje de entrada -> '))
vout = float(input('Inserte el valor del voltaje deseado en el divisor -> '))
N = 30 #Alternar entre 10 y 30
L = 28 #48, 40 y 28 bits funcionan 

def generador_de_individuos():
    temprow = []
    for row in range(0,N):
        for col in range(0,L):
            temprow.append(random.randint(0,1))
        poblacion_inicial.append(temprow)
        temprow = []

def bin2dec(bin_str):
    dec_num = 0
    potencia = 0
    bin_num = int(bin_str)
    
    while bin_num > 0:
        dec_num += 2 ** potencia * (bin_num % 10)
        bin_num //= 10
        potencia += 1
    return dec_num

def evaluacion_de_aptitud():
    global r1, r2, aptitud_lst, vin, rnum_1, rnum_2, inversion
    rnum_1 = []
    rnum_2 = []
    aptitud_lst = []
    inversion = []

    for individuo in poblacion_inicial:
        r1_temp = []
        r2_temp = []
        r1_bin_temp = ""
        r2_bin_temp = ""
        for bit in range(0, int(L/2)):
            r1_temp.append(individuo[bit])
            r1_bin_temp += str(individuo[bit])
        for bit in range(int(L/2), L):
            r2_temp.append(individuo[bit])
            r2_bin_temp += str(individuo[bit])
        r1.append(r1_temp)
        r2.append(r2_temp)
        rnum_1.append(bin2dec(r1_bin_temp))
        rnum_2.append(bin2dec(r2_bin_temp))

    for ind in range(N):
        error = 0
        salida1 = (vin*rnum_1[ind]) / (rnum_1[ind] + rnum_2[ind])
        salida2 = (vin*rnum_2[ind]) / (rnum_2[ind] + rnum_1[ind])
        error1 = abs(salida1 - vout)
        error2 = abs(salida2 - vout)

        if error1 < error2:
            error = error1
            inversion.append(0)
        elif error1 == error2:
            error = error1
            inversion.append(0)
        elif error2 < error1:
            error = error2
            inversion.append(1)

        exito = (1 - (error/vout)) * 100
        aptitud_lst.append(exito)

def ruleta_y_seleccion():
    global poblacion_copy, elite
    elite = []
    poblacion_copy = []
    tickets_array = []
    ruleta = []
    for apt in aptitud_lst:
        tickets = (apt * 100)/sum(aptitud_lst)
        if tickets - math.floor(tickets) >= 0.5:
            tickets_array.append(math.ceil(tickets))
        else:
            tickets_array.append(math.floor(tickets))

    for ticket_num in range(len(tickets_array)):
        for ticket in range(0,tickets_array[ticket_num]):
            ruleta.append(poblacion_inicial[ticket_num])
    
    apti_copy = list(aptitud_lst)
    inicial_temp = list(poblacion_inicial)

    max_index = apti_copy.index(max(apti_copy))
    individuo_elite = inicial_temp.pop(max_index)
    elite.append(individuo_elite)
    poblacion_copy.append(individuo_elite)
    apti_copy.pop(max_index)
    max_index = apti_copy.index(max(apti_copy))
    individuo_elite = inicial_temp.pop(max_index)
    elite.append(individuo_elite)
    poblacion_copy.append(individuo_elite)

    for elemento in range(0,N-2):
        random_ind = random.randint(0,(len(ruleta)-1))
        poblacion_copy.append(ruleta[random_ind])

def cruce_aleatorio():
    global poblacion_hijos
    poblacion_hijos = []
    pareja_temp = []
    for copia_ind in range(int(N/2)):
        punto_aleatorio = random.randint(1,L-2)
        pareja_temp.append(poblacion_copy[0])
        pareja_temp.append(poblacion_copy[1])
        poblacion_copy.pop(0)
        poblacion_copy.pop(0)
        poblacion_hijos.append(pareja_temp[0][0:punto_aleatorio] + pareja_temp[1][punto_aleatorio:L])
        poblacion_hijos.append(pareja_temp[1][0:punto_aleatorio] + pareja_temp[0][punto_aleatorio:L])
        pareja_temp = []

def mutacion():
    rand_mut = random.randint(1,100)
    if rand_mut <= 20:
        rand_fila = random.randint(0,(N-1))
        rand_col = random.randint(0,(L-1))
        individuo_al = poblacion_hijos[rand_fila][rand_col]
        if individuo_al == 0:
            poblacion_hijos[rand_fila][rand_col] = 1
        elif individuo_al == 1:
            poblacion_hijos[rand_fila][rand_col] = 0

def main():
    global iteracion, iteraciones, poblacion_inicial
    start = time.time()
    generador_de_individuos()
    evaluacion_de_aptitud()

    # print('--Primera Generacion--')
    # for ind in range(0,N):
    #     print(F'Individuo {ind}: {poblacion_inicial[ind]}   Aptitud: {aptitud_lst[ind]}')
    #     print(F'Resultado {ind}: R1 = {rnum_1[ind]}    R2 = {rnum_2[ind]}')

    ruleta_y_seleccion()
    cruce_aleatorio()
    mutacion()

    for iteraciones in range(0,iteraciones):
        poblacion_inicial = poblacion_hijos
        evaluacion_de_aptitud()
        ruleta_y_seleccion()
        cruce_aleatorio()
        mutacion()
        iteracion += 1

    end = time.time()

    print(F'{iteracion} iteraciones en {end-start} segundos')

    print('--Posibles valores de resistencias--')
    for ind in range(0,N):
        if aptitud_lst[ind] > 98:
            if inversion[ind] == 0:
                print(F'R1 = {rnum_1[ind]}    R2 = {rnum_2[ind]}    {aptitud_lst[ind]}% de éxito')
            elif inversion[ind] == 1:
                print(F'R1 = {rnum_2[ind]}    R2 = {rnum_1[ind]} {aptitud_lst[ind]}% de éxito')

if __name__ == "__main__":
    main()
