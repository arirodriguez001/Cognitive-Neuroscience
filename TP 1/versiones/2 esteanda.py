from psychopy import visual, core, event
import random

# Crear una ventana
win = visual.Window([1200, 700], fullscr=True, monitor='testMonitor', units='norm')

# Crear una lista de letras
letras = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']  # 21 letras

# Función para mostrar una pantalla de instrucciones
def mostrar_instrucciones(texto):
    texto_instrucciones = visual.TextStim(win, text=texto, wrapWidth=1.8, height=0.09)
    texto_instrucciones.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

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
        core.wait(0.01)
    core.wait(10)

# Función para chequear si se presionó la tecla 'Q'
def chequear_salida():
    keys = event.getKeys()
    if 'q' in keys:
        win.close()
        core.quit()
        
# Función para la pantalla de prueba
def pantalla_prueba():
    for _ in range(5):
        letras_seleccionadas = random.sample(letras, 7)
        mostrar_letras(letras_seleccionadas)
        chequear_salida()
        letra_pregunta = random.choice(letras)
        pregunta = f"¿Estaba la letra {letra_pregunta}? (derecha para sí, izquierda para no)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()
        # Puedes añadir lógica para registrar la respuesta si es necesario
        
def pantalla_preparacion():
    instrucciones_preparacion = (
        "Ahora comienza la sesión de práctica. A continuación, verás 21 tarjetas con letras. "
        "Presiona la barra espaciadora para comenzar el juego."
    )
    mostrar_instrucciones(instrucciones_preparacion)

        
# Generar preguntas combinadas y aleatorizadas
def generar_preguntas_combinadas():
    posiciones = list(range(7))  # Posiciones de 0 a 6 (correspondientes a las posiciones 1 a 7)
    preguntas_posicion = posiciones * 3  # Tres preguntas por cada posición
    random.shuffle(preguntas_posicion)  # Aleatorizar el orden de las preguntas

    preguntas_combinadas = []

    # Crear 21 preguntas sobre letras presentes en la serie
    for _ in range(21):
        letras_seleccionadas = random.sample(letras, 7)
        posicion_pregunta = preguntas_posicion.pop()
        letra_pregunta = letras_seleccionadas[posicion_pregunta]
        
        # Añadir la pregunta sobre la letra presente en la serie
        preguntas_combinadas.append((letras_seleccionadas, letra_pregunta, True))  # (serie de letras, letra, está presente)

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

# Función para ejecutar las preguntas combinadas (30 pantallas en total)
def ejecutar_preguntas(preguntas_combinadas):
    for letras_seleccionadas, letra_pregunta, es_presente in preguntas_combinadas:
        mostrar_letras(letras_seleccionadas)
        chequear_salida()
        
        # Pregunta sobre la letra
        pregunta = f"¿Estaba la letra {letra_pregunta}? (derecha para sí, izquierda para no)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()
        # Aquí se puede agregar lógica para registrar la respuesta si es necesario

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

# Ejecución del experimento
mostrar_instrucciones(
    "En este experimento aparecerán un total de siete letras en cada pantalla. "
    "Una vez mostrada la fila completa, las letras se borrarán de la pantalla y se le pedirá que identifique si una letra aparecía en esa fila. "
    "Si la letra indicada aparecía, haga click en la flecha de dirección derecha. "
    "En caso contrario, haga click en la flecha de dirección izquierda.\n"
    "\nPresione la barra espaciadora para iniciar una sesión de práctica del experimento"
)
pantalla_prueba()
pantalla_preparacion()
# Generar y ejecutar preguntas combinadas (21 sobre letras presentes + 9 sobre letras no presentes)
preguntas_combinadas = generar_preguntas_combinadas()
ejecutar_preguntas(preguntas_combinadas)

pantalla_felicitacion()

# Cerrar la ventana
win.close()
core.quit()
