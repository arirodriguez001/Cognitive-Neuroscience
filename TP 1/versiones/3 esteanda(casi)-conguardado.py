from psychopy import visual, core, event, data, gui
import random
import numpy as np
import pandas as pd
import time
from time import gmtime, strftime
#nota: faltaria el tiempo de rta y el gui

# Función para chequear si se presionó la tecla 'Q'
def chequear_salida():
    keys = event.getKeys()
    if 'q' in keys:
        win.close()
        core.quit()

#PANTALLAS

# Pantalla de instrucciones
def mostrar_instrucciones(texto):
    texto_instrucciones = visual.TextStim(win, text=texto, wrapWidth=1.8, height=0.09)
    texto_instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

#Pantalla de preparación
def pantalla_preparacion():
    instrucciones_preparacion = (
        "Ahora comienza la sesión de práctica. A continuación, verás 21 tarjetas con letras. "
        "Presiona la barra espaciadora para comenzar el experimento."
    )
    mostrar_instrucciones(instrucciones_preparacion)
    
# Pantalla de felicitación final
def pantalla_felicitacion():
    felicitacion = (
        "¡Felicidades! Has completado el experimento. "
        "Presiona la tecla 'Q' para salir."
    )
    texto_felicitacion = visual.TextStim(win, text=felicitacion, wrapWidth=1.8, height=0.09)
    texto_felicitacion.draw()
    win.flip()
    event.waitKeys(keyList=['q'])

#EXPERIMENTO

# Crear una lista de letras
letras = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']  # 21 letras

# Función para mostrar letras una a una, manteniendo las anteriores
def mostrar_letras(letras_seleccionadas):
    num_letras = len(letras_seleccionadas)
    total_espacio = 0.4  # Espacio total utilizado para letras
    espacio = total_espacio / (num_letras - 1) if num_letras > 1 else total_espacio
    x_start = -total_espacio / 2  # Centro de la ventana menos la mitad del espacio total

    textos = []
    for i, valor in enumerate(letras_seleccionadas):
        x_pos = x_start + i * espacio
        texto = visual.TextStim(win, text=valor, pos=(x_pos, 0), height=0.1)
        textos.append(texto)
        for t in textos:
            t.draw()
        win.flip()
        core.wait(0.3)
    core.wait(0.8)       #tiempos de las letras

# Función para correr la PRUEBA
def pantalla_prueba():
    for _ in range(5):
        letras_seleccionadas = random.sample(letras, 7)
        mostrar_letras(letras_seleccionadas)
        chequear_salida()
        letra_pregunta = random.choice(letras)
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n(flecha izquierda para no, flecha derecha para sí)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()

#info de guardado

numtrials= 30 #cantidad total de pantallas/trials
# variables/listas donde vamos a guardar la info 
data_letras_seleccionadas = []
data_posicion_pregunta = []
data_respuesta = []


# Generar preguntas combinadas y aleatorizadas
def generar_preguntas_combinadas():
    posiciones = list(range(7))  # Posiciones de 0 a 6 (correspondientes a las posiciones 1 a 7)
    preguntas_posicion = posiciones * 3  # Tres preguntas por cada posición
    random.shuffle(preguntas_posicion)  # Aleatorizar el orden de las preguntas

    preguntas_combinadas = []

    # Crear 21 preguntas sobre letras presentes en la serie
    for _ in range(21):
        letras_seleccionadas = random.sample(letras, 7)             #queremos guardar estos datos y la respuesta. +tiempo de rtas maybe
        posicion_pregunta = preguntas_posicion.pop()
        letra_pregunta = letras_seleccionadas[posicion_pregunta]
        
        # Añadir la pregunta sobre la letra presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, True))  # (serie de letras, letra, está presente)

    # guardo la data
    data_letras_seleccionadas.append(letras_seleccionadas)
    data_posicion_pregunta.append(posicion_pregunta)            #todavia falta la data de la respuesta


    # Crear 9 preguntas sobre letras no presentes en la serie
    for _ in range(9):
        letras_seleccionadas = random.sample(letras, 7)
        letras_no_presentes = list(set(letras) - set(letras_seleccionadas))  # Letras que no están en la serie
        letra_pregunta = random.choice(letras_no_presentes)
        
        # Añadir la pregunta sobre la letra no presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, False))  # (serie de letras, letra, no está presente)

    # Aleatorizar todas las preguntas (21 + 9)
    random.shuffle(preguntas_combinadas)
    return preguntas_combinadas
    

# Función para correr el EXPERIMENTO (30 pantallas en total)
def ejecutar_preguntas(preguntas_combinadas):
    for letras_seleccionadas, letra_pregunta, es_presente in preguntas_combinadas:
        mostrar_letras(letras_seleccionadas)
        chequear_salida()
        
        # Pregunta sobre la letra
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n (no-si)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()
        else:
            if letra_pregunta in letras_seleccionadas: #si la letra esta
                if 'left' in respuesta:                  #y si responde que NO 
                    data_respuesta.append(0)         #guardar 0='mal'
                else:
                    data_respuesta.append(1)       #sino 1='bien'               #ver si conviene cambiar por unos y ceros
            else:
                data_respuesta.append(2)    #si la letra no aparece


#   EJECUCION
'''
#%% Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addText('Subejc info*')
dlg.addField('Subject ID:',initial='1')
id_inf = dlg.show()

if dlg.OK:
    # id_inf es una lista con los valores ingresados
    info = {
        'participant': id_inf[0]     
    }

#%%  Defino parametros
info = {} #a dictionary
#present dialog to collect info
info['participant'] = id_inf[0]

#%% Datos de salida
# Obtener nombre o código del participante
dlg = gui.Dlg(title="exp-7letras", pos=(200, 400))
dlg.addField('Participant #', 'Participante:')
    '''
    
# Directorio donde se van a guardar los datos (MODIFICAR!)
PARTICIPANT_FILENAME = '/Users/Usuario/Desktop/Anabella/neurociencia' + 'data_' + '1' + '.csv'

#corremos el experimento
win = visual.Window([1200, 700], fullscr=True, monitor='testMonitor', units='norm') # Crear una ventana
mostrar_instrucciones(
    "En este experimento aparecerán un total de siete letras en cada pantalla. "
    "Una vez mostrada la fila completa, las letras se borrarán de la pantalla y se le pedirá que identifique si una letra aparecía en esa fila. "
    "Si la letra indicada aparecía, presione la flecha de dirección derecha. "
    "En caso contrario, presione en la flecha de dirección izquierda.\n"
    "\nPresione la barra espaciadora para iniciar una sesión de práctica del experimento"
)
pantalla_prueba()
pantalla_preparacion()
preguntas_combinadas = generar_preguntas_combinadas() # Generar y ejecutar preguntas combinadas (21 sobre letras presentes + 9 sobre letras no presentes)
ejecutar_preguntas(preguntas_combinadas)
pantalla_felicitacion()

'''
#Guardar la data
data = {'Trial':np.arange(1,numtrials+1), '7letras':data_letras_seleccionadas, 'posicion':data_posicion_pregunta, 'respuesta':data_respuesta} #faltaria el tiempo de respuesta

df = pd.DataFrame(data) 

df.to_csv(PARTICIPANT_FILENAME)
'''
win.close() # Cerrar la ventana
core.quit()

