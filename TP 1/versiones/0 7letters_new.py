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
    total_espacio = 0.9  # Espacio total utilizado para letras
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
    core.wait(1.5)

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
        pregunta = f"¿La letra {letra_pregunta} estaba en la serie mostrada? (derecha para sí, izquierda para no)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()
        # Puedes añadir lógica para registrar la respuesta si es necesario

# Pantalla de preparación
def pantalla_preparacion():
    instrucciones_preparacion = (
        "Ahora comienza la sesión de práctica. A continuación, verás 20 tarjetas con letras. "
        "Presiona la barra espaciadora para comenzar el juego."
    )
    mostrar_instrucciones(instrucciones_preparacion)

# Función para el juego principal
def juego_principal():
    for _ in range(20):
        letras_seleccionadas = random.sample(letras, 7)
        mostrar_letras(letras_seleccionadas)
        chequear_salida()
        letra_pregunta = random.choice(letras)
        pregunta = f"¿La letra {letra_pregunta} estaba en la serie mostrada? (derecha para sí, izquierda para no)"
        texto_pregunta = visual.TextStim(win, text=pregunta, height=0.09)
        texto_pregunta.draw()
        win.flip()
        respuesta = event.waitKeys(keyList=['left', 'right', 'q'])
        if 'q' in respuesta:
            win.close()
            core.quit()
        # Puedes añadir lógica para registrar la respuesta si es necesario

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
juego_principal()
pantalla_felicitacion()

# Cerrar la ventana
win.close()
core.quit()
