from contextlib import nullcontext
from turtle import color
from xml.etree.ElementTree import tostring
import PySimpleGUI as sg
import math
import random
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
vin = 0
vout = 0
N = 30 #Alternar entre 10 y 30
L = 28 #48, 40 y 28 bits funcionan
epocas = 100
run_again = False
r1_final = 0
r2_final = 0
aptitud_final = 0

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

def algotithm():
    global iteracion, iteraciones, poblacion_inicial, r1_final, r2_final, aptitud_final, epocas, run_again

    apt_flag = False

    start = time.time()
    for epoca in range(epocas):
        generador_de_individuos()
        evaluacion_de_aptitud()
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

        print('--Posibles valores de resistencias--')
        for ind in range(0,N):
            if aptitud_lst[ind] > 98:
                if inversion[ind] == 0:
                    print(F'R1 = {rnum_1[ind]}    R2 = {rnum_2[ind]}    {aptitud_lst[ind]}% de exactitud')
                    r1_final = rnum_1[ind]
                    r2_final = rnum_2[ind]
                    aptitud_final = aptitud_lst[ind]
                elif inversion[ind] == 1:
                    print(F'R1 = {rnum_2[ind]}    R2 = {rnum_1[ind]} {aptitud_lst[ind]}% de exactitud')
                    r1_final = rnum_2[ind]
                    r2_final = rnum_1[ind]
                    aptitud_final = aptitud_lst[ind]
                apt_flag = True
        if apt_flag:
            break
        else:
            run_again = True
    end = time.time()
    print(F'{end-start} segundos')

def build_gui():
    global vin, vout, r1_final, r2_final, aptitud_final

    sg.LOOK_AND_FEEL_TABLE['CustomTheme'] = {
        'BACKGROUND': '#1c1B22',
        'TEXT': '#e2e2e2', # #4550e6', #7f83e7, #7679d3, #6a5be1
        'INPUT': '#2b2a33',
        'TEXT_INPUT': '#e2e2e2',
        'SCROLL': '#2b2a33',
        'BUTTON': ('#e2e2e2', '#2b2a33'), # #6a5be1
        'PROGRESS': ('green', '#e2e2e2'), 
        'BORDER': 0, 'SLIDER_DEPTH': 0, 
        'PROGRESS_DEPTH': 0 }

    sg.theme('CustomTheme')

    #Column construction#
    

    layout = [
        [sg.Text('VolDivAI', font = ('Trebuchet MS', 20, 'bold'), text_color = '#6a5be1')],
        [sg.Text('Voltaje de entrada', font = ('Trebuchet MS', 15))],
        [sg.InputText(key='__VIN__', font = ('Trebuchet MS', 14))],
        [sg.Text('Voltaje de salida', font = ('Trebuchet MS', 15))],
        [sg.InputText(key='__VOUT__', font = ('Trebuchet MS', 14))],
        [sg.Text('', font = ('Trebuchet MS', 14,  'bold'), text_color = '#6a5be1', key = '__R1__')],
        [sg.Text('', font = ('Trebuchet MS', 14, 'bold'), text_color = '#6a5be1', key = '__R2__')],
        [sg.Text('', font = ('Trebuchet MS', 12), text_color = '#6a5be1', key = '__APT__')],
        [sg.Button('Calcular', size=(10,1), font = ('Trebuchet MS', 12, 'bold'), mouseover_colors = '#6a5be1')], #, button_color = '#6a5be1'
        [sg.Button('Limpiar', size=(10,1), font = ('Trebuchet MS', 12, 'bold'))],
        [sg.Button('Salir', size=(10,1), font = ('Trebuchet MS', 12, 'bold'), mouseover_colors = '#ef5350')]
    ]

    window = sg.Window('VolDivAI', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break
        elif event == 'Limpiar':
            window['__VIN__'].update('')
            window['__VOUT__'].update('')
            window['__R1__'].update('')
            window['__R2__'].update('')
            window['__APT__'].update('')
        elif event == 'Calcular':
            if values['__VIN__'] != "" or values['__VOUT__'] != "":    
                try:
                    vin = float(values['__VIN__'])
                    vout = float(values['__VOUT__'])
                    algotithm()
                    r1_string = 'R1 = ' + str(r1_final)
                    r2_string = 'R1 = ' + str(r2_final)
                    aptitud_string = str(round(aptitud_final, 2)) + '% de exactitud'
                    window['__R1__'].update(r1_string)
                    window['__R2__'].update(r2_string)
                    window['__APT__'].update(aptitud_string)
                except:
                    window['__VIN__'].update('')
                    window['__VOUT__'].update('')
                    window['__R1__'].update('')
                    window['__R2__'].update('')
                    window['__APT__'].update('')
                    sg.popup('Algún campo contiene un valor no numérico', title = 'Error')    
            elif values['__VIN__'] == "" or values['__VOUT__'] == "":
                sg.popup('Algún campo está vacío', title = 'Error')

            if run_again:
                window['__VIN__'].update('')
                window['__VOUT__'].update('')
                window['__R1__'].update('')
                window['__R2__'].update('')
                window['__APT__'].update('')
                sg.popup('No se encotnró un resultado satisfactorio\n Por favor vuelve a intentar')
                window.close()


    window.close()

def main():
    build_gui()

if __name__ == '__main__':
    main()