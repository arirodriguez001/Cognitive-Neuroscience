from psychopy import visual, core, event
import random

# Crear una ventana
win = visual.Window([1200, 700])

# Crear una lista de letras
letras = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']  # 21 letras

#----------------------------PANTALLA DE INICIO-------------------------------------
# Texto que se mostrará en la pantalla
instrucciones = (
    "En este experimento aparecerán un total de siete letras en cada pantalla. "
    "\n Una vez mostrada la fila completa, las letras se borrarán de la pantalla y se le pedirá que identifique si una letra aparecía en esa fila. "
    "Si la letra indicada aparecía, haga click en la flecha de dirección derecha. "
    "En caso contrario, haga click en la flecha de dirección izquierda.\n"
    "\n Presione la barra espaciadora para iniciar una sesión de práctica del experimento"
)

# Crear un objeto de texto
texto_explic = visual.TextStim(win, text=instrucciones, wrapWidth=1.8, height=0.09) 

# Dibujar el texto en la ventana y mostrarlo
texto_explic.draw()
win.flip()

# Esperar a que el usuario presione la barra espaciadora para continuar
event.waitKeys(keyList=['space'])

# Limpiar la pantalla
win.flip()

#-----------------------------VECTOR DE LETRAS------------------------------------
# Coordenada inicial para la primera letra
x_pos = -0.5  # Coordenada en el eje x (ajusta según sea necesario)

# Tamaño del texto
tamano_texto = 0.1

# Seleccionar 7 letras aleatorias de la lista de letras
letras_seleccionadas = random.sample(letras, 7)

# Crear una lista para almacenar los objetos de texto
textos = []

# Mostrar letras una a una, manteniendo las anteriores
for i, valor in enumerate(letras_seleccionadas): # i recibe el índice del elemento actual en la lista, valor recibe la letra en sí
    # Crear un objeto de texto para el valor actual
    texto = visual.TextStim(win, text=valor, pos=(x_pos + i * 0.15, 0), height=tamano_texto)
    textos.append(texto)  # Añadir el texto a la lista
    
    # Dibujar todos los textos acumulados en la pantalla
    for t in textos:
        t.draw()
    win.flip()  # Actualizar la ventana para mostrar los textos actuales
    
    # Esperar 1 segundo antes de mostrar la siguiente letra
    core.wait(1)

# Mantener la ventana abierta por un tiempo adicional para ver todas las letras
core.wait(2)

# Cerrar la ventana
win.close()
core.quit()
