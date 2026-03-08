from psychopy import visual, core, event, data, gui
import random
import numpy as np
import pandas as pd
import time
from time import gmtime, strftime

#PANTALLAS

# Pantalla de instrucciones
def mostrar_instrucciones(texto):
    texto_instrucciones = visual.TextStim(win, text=texto, wrapWidth=1.8, height=0.09)
    texto_instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

#Pantallas de preparación

def pantalla_preprueba():
    preprueba = (
        "Presiona la barra espaciadora para comenzar una PRUEBA de cinco intentos. "
        "\n Preste atención a qué letras ve."
    )
    texto = visual.TextStim(win, text=preprueba, wrapWidth=1.8, height=0.09)
    texto.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
def pantalla_preexp():
    instrucciones_preparacion = (
        "Finalizó la sesión de prueba."
        "\n \n Presiona la barra espaciadora para comenzar el experimento."
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

letras = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']  # 21 letras
timer = core.Clock() 

def mostrar_letras(letras_seleccionadas):
    num_letras = len(letras_seleccionadas)
    total_espacio = 0.8  # Espacio total para letras
    espacio = total_espacio / (10 - 1) if num_letras > 1 else total_espacio  # Espacio distribuido entre 5 letras
    x_start = -total_espacio / 2  # Centro de la ventana menos la mitad del espacio total
    textos = [None] * 5  # Lista con 5 posiciones vacías inicialmente
    index = 0  # Contador de letras que se van a mostrar

    for i, valor in enumerate(letras_seleccionadas):
        if index < 5:
            # Para las primeras 5 letras, las colocamos en las primeras 5 posiciones
            x_pos = x_start + (index) * espacio
            texto = visual.TextStim(win, text=valor, pos=(x_pos, 0), height=0.15)
            textos[index] = texto  # Coloca la letra en la posición correspondiente de los primeros 5 lugares
        else:
            # Después de la quinta letra, las letras se colocan a la derecha.
            x_pos = x_start + (index) * espacio
            texto = visual.TextStim(win, text=valor, pos=(x_pos, 0), height=0.15)
            texto.draw() 
            textos.pop(0)  # Eliminar la primera letra (la más antigua)
            textos.append(texto)  # Añadir la nueva letra en la última posición
        
        # Dibujar las letras en la pantalla (las primeras 5 que no están en None)
        for t in textos:
            if t is not None:  # Solo dibujar las letras que no son None
                t.draw()

        # Actualizar la ventana
        win.flip()

        # Esperar 0.2 segundos antes de mostrar la siguiente letra
        core.wait(0.2)

        index += 1  # Aumentamos el contador para ir a la siguiente letra

    # Mantener las letras visibles durante 1.5 segundos después de mostrar la última
    core.wait(1.5)

# Función para correr la PRUEBA
def pantalla_prueba():
    for _ in range(5):
        letras_seleccionadas = random.sample(letras, 10)
        mostrar_letras(letras_seleccionadas)
        letra_pregunta = random.choice(letras)
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n(izquierda para no, derecha para sí)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()


# listas donde vamos a guardar la info 
data_10letras = []
data_letra_pregunta = []
data_posicion = []
data_respuesta = []
data_tiempo_rta = []


# Generar preguntas combinadas y aleatorizadas
def generar_preguntas_combinadas():
    posiciones = list(range(10))  # cantidad de posiciones/letras
    preguntas_posicion = posiciones * 2  # 2 preguntas por cada posición
    random.shuffle(preguntas_posicion)  # Aleatorizar el orden de las preguntas

    preguntas_combinadas = []

    # Crear 20 preguntas sobre letras presentes en la serie
    for _ in range(20): 
        letras_seleccionadas = list(random.sample(letras, 10))             
        posicion_pregunta = preguntas_posicion.pop()
        letra_pregunta = letras_seleccionadas[posicion_pregunta]
        
        # Añadir la pregunta sobre la letra presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, posicion_pregunta, True))


    # Crear 10 preguntas sobre letras no presentes en la serie
    for _ in range(10):                                                                               
        letras_seleccionadas = random.sample(letras, 10)
        letras_no_presentes = list(set(letras) - set(letras_seleccionadas))  # Letras que no están en la serie
        letra_pregunta = random.choice(letras_no_presentes)
        
        # Añadir la pregunta sobre la letra no presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, posicion_pregunta, False))

    # Aleatorizar todas las preguntas (20+10)
    random.shuffle(preguntas_combinadas)
    return preguntas_combinadas
    

# Función para correr el EXPERIMENTO (30 pantallas en total)
def ejecutar_preguntas(preguntas_combinadas):
    for letras_seleccionadas, letra_pregunta, posicion_pregunta, es_presente  in preguntas_combinadas:
        mostrar_letras(letras_seleccionadas)
        
        #Guardado
        data_10letras.append(letras_seleccionadas) 
        data_letra_pregunta.append(letra_pregunta)
        data_posicion.append(posicion_pregunta+1)
        
        # Pregunta sobre la letra
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n (no-si)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        timer.reset()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        resp_time = timer.getTime()
        
        #guardado
        data_tiempo_rta.append(resp_time)
        if 'left' in respuesta: #si responde NO
            if letra_pregunta in letras_seleccionadas:
                data_respuesta.append(0)                #0='mal'
            else:
                data_respuesta.append(2)                #2=no estaba  
        elif 'right' in respuesta: #si responde SI
            if letra_pregunta in letras_seleccionadas:
                data_respuesta.append(1)                #1='bien'
            else:
                data_respuesta.append(3)                #3=falso si
        elif 'q' in respuesta:
            win.close()
            core.quit()


#   EJECUCION

# Obtener nombre o código del participante
dlg = gui.Dlg(title="Experimento 10-letras")
dlg.addField('archivo', 'Nombre')

SESSION = dlg.show() #dlg.show es un diccionario que guarda los inputs

if dlg.OK:
    ARCHIVO = SESSION['archivo']    #desde spyder anda con un 0
else:
        print('User cancelled')
        core.quit()

PARTICIPANT_FILENAME = 'C:/Users/mralf/OneDrive/Escritorio/Laboratorio Lucy/Neuro/TP final/'+ 'data10_' + str(ARCHIVO) + '.csv'

#corremos el experimento
win = visual.Window([1366, 768], fullscr=False, monitor='testMonitor', units='norm')
mostrar_instrucciones(
    "Lea atentamente."
    "\n\n En este experimento se le mostrarán 10 letras en la pantalla y luego"
    " se le preguntará si cierta letra estaba o no entre las que vió.\n"
    "Si cree que la letra indicada NO apareció, presione la flecha izquierda de su teclado. "
    "En caso contrario, si cree que SI, presione la flecha derecha.\n"
    "El procedimiento se repetirá sucesivamente treinta veces. (es rápido)\n"
    "\nPresione la barra espaciadora para continuar."
)
pantalla_preprueba()
pantalla_prueba()                                                    
pantalla_preexp()
preguntas_combinadas = generar_preguntas_combinadas() 
ejecutar_preguntas(preguntas_combinadas)
pantalla_felicitacion()

#guardado de la data
numtrials= 30 #cantidad total de pantallas                      
data = {'Trial':np.arange(1,numtrials+1), 'letras':data_10letras, 'pregunta':data_letra_pregunta, 'posicion':data_posicion, 'respuesta':data_respuesta, 'tiempo': data_tiempo_rta}
df = pd.DataFrame(data) 
df.to_csv(PARTICIPANT_FILENAME,index=False)
print(f"Archivo guardado exitosamente en {PARTICIPANT_FILENAME}")

# Cerrar todo
win.close()
core.quit()