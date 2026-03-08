from psychopy import visual, core, event, data, gui
import random
import numpy as np
import pandas as pd

# PANTALLAS

# Pantalla de instrucciones
def mostrar_instrucciones(texto):
    texto_instrucciones = visual.TextStim(win, text=texto, wrapWidth=1.8, height=0.09)
    texto_instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

# Pantallas de preparación
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

# EXPERIMENTO

letras = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
timer = core.Clock()

# Función para mostrar un "enfoque deslizante" en las letras
def mostrar_enfoque_deslizante(serie_letras):
    
    total_espacio = 0.6  # Espacio total para letras
    x_start = -total_espacio / 2  # Centro de la ventana menos la mitad del espacio total
    espacio = total_espacio / (7 - 1)  # Espacio distribuido entre 5 letras
    
    duracion_paso = 0.3  # Tiempo de cada paso (en segundos)

    # Crear objetos de texto para todas las letras
    textos = [
        visual.TextStim(
            win,
            text=letra,
            pos=[x_start + i * espacio, 0],  # Posición inicial de cada letra
            height=0.15,
            color="gray"  # Color inicial de las letras
        )
        for i, letra in enumerate(serie_letras)
    ]

    longitud = len(serie_letras)

    # Fase inicial: mostrar de 1 a 4 letras progresivamente
    for paso in range(1, 4):  # Mostrar 1, luego 2, luego 3 (detenemos antes de 4 para suavizar transición)
        for i, texto in enumerate(textos):
            if i < paso:  # Letras visibles según el paso
                texto.color = "white"
            else:
                texto.color = "gray"
            texto.draw()
        win.flip()
        core.wait(duracion_paso)

    # Fase deslizante: mantener 4 letras visibles (sin incluir la última repetición)
    for paso in range(longitud - 4):  # Desplazar hasta que falten 4 letras por mostrar
        for i, texto in enumerate(textos):
            if paso <= i < paso + 4:  # Letras visibles
                texto.color = "white"
            else:
                texto.color = "gray"
            texto.draw()
        win.flip()
        core.wait(duracion_paso)

    # Fase final: desaparecer de 4 a 1 letras (sin repetir el último estado)
    for paso in range(4, 0, -1):  # Mostrar 4, luego 3, luego 2, hasta 1 letra
        for i, texto in enumerate(textos):
            if i >= longitud - paso:  # Letras visibles
                texto.color = "white"
            else:  # Letras que ya no están visibles
                texto.color = "gray"
            texto.draw()
        win.flip()
        core.wait(duracion_paso)


# Función para correr la PRUEBA
def pantalla_prueba():
    for _ in range(5):
        letras_seleccionadas = random.sample(letras, 7)   # !!!!
        mostrar_enfoque_deslizante(letras_seleccionadas)  # Enfoque deslizante
        letra_pregunta = random.choice(letras)
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n(izquierda para no, derecha para sí)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()

# Listas donde vamos a guardar la info
data_7letras = []
data_letra_pregunta = []
data_posicion = []
data_respuesta = []
data_tiempo_rta = []

# Generar preguntas combinadas y aleatorizadas
def generar_preguntas_combinadas():
    posiciones = list(range(7))  # cantidad de posiciones/letras                    # !!!!
    preguntas_posicion = posiciones * 3  # 2 preguntas por cada posición            # !!!!
    random.shuffle(preguntas_posicion)  # Aleatorizar el orden de las preguntas

    preguntas_combinadas = []

    # Crear 21 preguntas sobre letras presentes en la serie # !!!!
    for _ in range(21):                                        # !!!!
        letras_seleccionadas = list(random.sample(letras, 7))  # !!!!           
        posicion_pregunta = preguntas_posicion.pop()
        letra_pregunta = letras_seleccionadas[posicion_pregunta]
        
        # Añadir la pregunta sobre la letra presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, posicion_pregunta, True))

    # Crear n preguntas sobre letras no presentes en la serie
    for _ in range(9):                                  # !!!!                                                            
        letras_seleccionadas = random.sample(letras, 7)# !!!!
        letras_no_presentes = list(set(letras) - set(letras_seleccionadas))  # Letras que no están en la serie
        letra_pregunta = random.choice(letras_no_presentes)
        
        # Añadir la pregunta sobre la letra no presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, posicion_pregunta, False))

    # Aleatorizar todas las preguntas (21+9)
    random.shuffle(preguntas_combinadas)
    return preguntas_combinadas

# Función para correr el EXPERIMENTO (30 pantallas en total)
def ejecutar_preguntas(preguntas_combinadas):
    for letras_seleccionadas, letra_pregunta, posicion_pregunta, es_presente in preguntas_combinadas:
        mostrar_enfoque_deslizante(letras_seleccionadas)  # Enfoque deslizante en el experimento
        
        # Guardado
        data_7letras.append(letras_seleccionadas) 
        data_letra_pregunta.append(letra_pregunta)
        data_posicion.append(posicion_pregunta + 1)
        
        # Pregunta sobre la letra
        pregunta = f"¿Estaba la letra {letra_pregunta}?\n (no-si)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        timer.reset()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        resp_time = timer.getTime()
        
        # Guardado
        data_tiempo_rta.append(resp_time)
        if 'left' in respuesta:  # si responde NO
            if letra_pregunta in letras_seleccionadas:
                data_respuesta.append(0)                # 0 = 'mal'
            else:
                data_respuesta.append(2)                # 2 = no estaba
        elif 'right' in respuesta:  # si responde SI
            if letra_pregunta in letras_seleccionadas:
                data_respuesta.append(1)                # 1 = 'bien'
            else:
                data_respuesta.append(3)                # 3 = falso si
        elif 'q' in respuesta:
            win.close()
            core.quit()

# EJECUCIÓN

# Obtener nombre o código del participante
dlg = gui.Dlg(title="Experimento 7-letras") # !!!!
dlg.addField('archivo', 'Nombre')

SESSION = dlg.show()  #dlg.show es un diccionario que guarda los inputs

if dlg.OK:
    ARCHIVO = SESSION['archivo']  #desde spyder anda con un 0
else:
    print('User cancelled')
    core.quit()

PARTICIPANT_FILENAME = '/Users/Usuario/Desktop/Anabella/neurociencia/' + 'data7_' + str(ARCHIVO) + '.csv' # !!!!

# Correr el experimento
win = visual.Window([1366, 768], fullscr=True, monitor='testMonitor', units='norm')
mostrar_instrucciones(
    "Lea atentamente."
    "\n\n En este experimento se le mostrarán 7 letras en la pantalla y luego"# !!!!
    " se le preguntará si cierta letra estaba o no entre las que vio.\n"
    "Si cree que la letra indicada NO apareció, presione la flecha izquierda de su teclado. "
    "En caso contrario, si cree que SÍ, presione la flecha derecha.\n"
    "El procedimiento se repetirá sucesivamente treinta veces.\n"# !!!!
    "\nPresione la barra espaciadora para continuar."
)
pantalla_preprueba()
pantalla_prueba()                                                    
pantalla_preexp()
preguntas_combinadas = generar_preguntas_combinadas()  # Generar y ejecutar preguntas combinadas
ejecutar_preguntas(preguntas_combinadas)

# Guardar datos al finalizar
df = pd.DataFrame({
    'Serie 7-letras': data_7letras,# !!!!
    'Letra-pregunta': data_letra_pregunta,
    'Posición': data_posicion,
    'Respuesta': data_respuesta,
    'RT': data_tiempo_rta
})

df.to_csv(PARTICIPANT_FILENAME, index=False)
print('Finalizado. Datos guardados en {PARTICIPANT_FILENAME}.')

# Pantalla de felicitación
pantalla_felicitacion()
win.close()
core.quit()
