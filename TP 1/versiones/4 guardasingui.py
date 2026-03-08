from psychopy import visual, core, event, data, gui
import random
import numpy as np
import pandas as pd
import time
from time import gmtime, strftime
                                                            #NOTA: cambie los numeros para que la prueba fuese mas corta
                                                            #y chequear lo del guardado. Todo lo cambiado dice CAMBIADO. 
                                                            #faltaria automatizar el cambio de nombre del archivo cada vez
                                                            #que se guarda (quizas usando el gui) y ver si medir los tiempos
                                                            #de respuesta (yo diria de hacerlo)

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
        "Presiona la barra espaciadora para salir."
    )
    texto_felicitacion = visual.TextStim(win, text=felicitacion, wrapWidth=1.8, height=0.09)
    texto_felicitacion.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

#EXPERIMENTO

#ista de letras
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


# listas donde vamos a guardar la info 
data_7letras = []
data_letra_pregunta = []
data_respuesta = []

# Generar preguntas combinadas y aleatorizadas
def generar_preguntas_combinadas():
    posiciones = list(range(2))  # Posiciones de 0 a 6 (correspondientes a las posiciones 1 a 7)     CAMBIADO. era 7
    preguntas_posicion = posiciones * 3  # Tres preguntas por cada posición
    random.shuffle(preguntas_posicion)  # Aleatorizar el orden de las preguntas

    preguntas_combinadas = []

    # Crear 21 preguntas sobre letras presentes en la serie
    for _ in range(4):                                                                                #CAMBIADO, 21
        letras_seleccionadas = list(random.sample(letras, 7))             
        posicion_pregunta = preguntas_posicion.pop()
        letra_pregunta = letras_seleccionadas[posicion_pregunta]
        
        # Añadir la pregunta sobre la letra presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, True))  # (serie de letras, letra, está presente)


    # Crear 9 preguntas sobre letras no presentes en la serie
    for _ in range(2):                                                                                #CAMBIADO,9
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
        
        #Guardado
        data_7letras.append(letras_seleccionadas) 
        data_letra_pregunta.append(letra_pregunta) 
        
        chequear_salida()
        
        # Pregunta sobre la letra
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n (no-si)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        #guardado
        if 'left' in respuesta: #si responde NO
            if letra_pregunta in letras_seleccionadas: #si la letra esta
                data_respuesta.append(0)                #guardar 0='mal'
            else:
                data_respuesta.append(2)                
        elif 'right' in respuesta: #si responde SI
            if letra_pregunta in letras_seleccionadas:
                data_respuesta.append(1)                 #1='bien'
            else:
                data_respuesta.append(3)                #3= falso si
        elif 'q' in respuesta:
            win.close()
            core.quit()


#   EJECUCION

''' #esto fue un intento de gui que no me quedo, es un mamarracho
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


#corremos el experimento
win = visual.Window([1200, 700], fullscr=True, monitor='testMonitor', units='norm') # Crear una ventana
mostrar_instrucciones(
    "En este experimento aparecerán un total de siete letras en cada pantalla. "
    "Una vez mostrada la fila completa, las letras se borrarán de la pantalla y se le pedirá que identifique si una letra aparecía en esa fila. "
    "Si la letra indicada aparecía, presione la flecha de dirección derecha. "
    "En caso contrario, presione en la flecha de dirección izquierda.\n"
    "\nPresione la barra espaciadora para iniciar una sesión de práctica del experimento"
)
#pantalla_prueba()                                                     #CAMBIADO
pantalla_preparacion()
preguntas_combinadas = generar_preguntas_combinadas() # Generar y ejecutar preguntas combinadas (21 sobre letras presentes + 9 sobre letras no presentes)
ejecutar_preguntas(preguntas_combinadas)
pantalla_felicitacion()

#Guardar la data
PARTICIPANT_FILENAME = '/Users/Usuario/Desktop/Anabella/neurociencia/data_1.csv' #IR CAMBIANDO DATA_2 O AUTOMATIZAR, IDEALMENTE CON EL GUI (pero habia un archivo de enzo que no lo usaba asi que no es necesario creo)

#/Users/Usuario/Desktop/Anabella/neurociencia
#
#los suyos

numtrials= 6 #cantidad total de pantallas/trials                        #CAMBIADO
data = {'Trial':np.arange(1,numtrials+1), 'letras':data_7letras, 'pregunta':data_letra_pregunta, 'respuesta':data_respuesta} #faltaria el tiempo de respuesta
df = pd.DataFrame(data) 
df.to_csv(PARTICIPANT_FILENAME,index=False)
print(f"Archivo guardado exitosamente en {PARTICIPANT_FILENAME}")

core.wait(1)
win.close() # Cerrar la ventana

