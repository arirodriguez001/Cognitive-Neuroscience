import numpy as np
import pandas as pd
from random import randint, shuffle
from psychopy import visual, event, core, gui
import random
import time
from time import gmtime, strftime

# Attentional blink con targets numéricos en secuencias de letras
# Los lags varían entre 1 y 7 (en terminos de letras en la secuencia)
# El target inicial (T1) se inserta en la secuencia de letras al azar entre las posiciones 6 y 9
# El segundo target (T2) se inserta después de T1 de acuerdo al lag correspondiente
# Luego de T2, las secuencias se extienden al azar por 1 a 3 letras más antes de terminar


# Creamos los "streams" (secuencias de letras y targets) para dos casos:
# 1) Secuencias de práctica (solamente 7 trials)
# 2) Experimento (140 trials)

lags = [1]*20 + [2]*20 + [3]*20 + [4]*20 + [5]*20 + [6]*20 + [7]*20   # definimos la cantidad de cada uno de los lags

NUMTRIALS = len(lags) # el número de trials equivale a la cantidad total de lags (140)

shuffle(lags)   # randomizamos el orden de los lags

# variables donde vamos a cuardar los streams de práctica, sus targets, lags y posiciones en la secuencai 
practice_trials = []
practice_targets = []
practice_lags = []
practice_positions = []

for trial in np.arange(7): # iteramos sobre la cantidad de trials de práctica

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'U', 'W', 'V', 'Y'] # letras (notar que faltan algunas)
    targets = ['2','3','4','5','6','7','8','9']  # targets
    shuffle(targets) # randomizar los targets

    # primero creo un stream de longitud 21 con letras distintas
    
    stream = [letters[randint(0, 19)]]

    for i in np.arange(1,21):  # esto me asegura que las letras que agrego no se repitan
        ind = randint(0, 19)
        candidate = letters[ind]
        while candidate == stream[i-1]:
            candidate = letters[randint(0, 19)]
        stream.append(candidate)

    # elije el lag correspondiente al trial 
    lag = lags[trial]
    # decide los targets correspondientes al trial
    T1 = targets.pop()
    T2 = targets.pop()
    # determina la posición de T1 y lo inserta en la secuencia
    T1_pos = [6,9]
    shuffle(T1_pos)
    position_T1 = T1_pos.pop()
    stream[position_T1] = T1
    stream[position_T1 + lag+1] = T2 # inserta el T2 de acuerdo al lag
    T2_pos = [1,3] # extensiones posibles de la secuencia luego de T2
    shuffle(T2_pos)
    position_T2 = T2_pos.pop()
    stream = stream[0:position_T1 + lag+1+position_T2+1] # corta la secuencia dependiendo de la extensión luego de T2
    # guarda todo 
    practice_trials.append(stream) 
    practice_targets.append([T1,T2])
    practice_lags.append(lag)
    practice_positions.append([position_T1,position_T2])
    
    
# Este código repite lo anterior pero para los trials del experimento "real" (NUMTRIALS)

lags = [1]*20 + [2]*20 + [3]*20 + [4]*20 + [5]*20 + [6]*20 + [7]*20
shuffle(lags)
real_trials = []
real_targets = []
real_lags = []
real_positions = []

for trial in np.arange(NUMTRIALS):

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'U', 'W', 'V', 'Y']
    targets = ['2','3','4','5','6','7','8','9']
    shuffle(targets)
    
    stream = [letters[randint(0, 19)]]
    for i in np.arange(1,21):
        ind = randint(0, 19)
        candidate = letters[ind]
        while candidate == stream[i-1]:
            candidate = letters[randint(0, 19)]
        stream.append(candidate)
    lag = lags[trial]
    # decide los targets
    T1 = targets.pop()
    T2 = targets.pop()
    T1_pos = [6,9]
    shuffle(T1_pos)
    position_T1 = T1_pos.pop()
    stream[position_T1] = T1
    stream[position_T1 + lag+1] = T2
    T2_pos = [1,3]
    shuffle(T2_pos)
    position_T2 = T2_pos.pop()
    stream = stream[0:position_T1 + lag+1+position_T2+1]
    real_trials.append(stream)
    real_targets.append([T1,T2])
    real_lags.append(lag)
    real_positions.append([position_T1,position_T2])
    

# El siguiente código implementa el experimento en Psychopy

# Obtener nombre o código del participante
dlg = gui.Dlg(title="Attentional Blink", pos=(200, 400))
dlg.addField('Participant #', 999)

# Abrir la interfaz
SESSION = dlg.show()  
if dlg.OK:
    SESSION_TIMESTAMP = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    PARTICIPANT = SESSION[0]
else:
    print('User cancelled')
    core.quit()
    
# Directorio donde se van a guardar los datos (MODIFICAR!)
PARTICIPANT_FILENAME = '/Users/enzotagliazucchi/Downloads/' + 'data_' + str(PARTICIPANT) + '.csv'
    
# Inicializa una ventana donde se va a correr el experimento
win = visual.Window([2560, 1440],
                    monitor='Dell precision',
                    fullscr=True,
                    screen=1,
                    units='norm',
                    color='gainsboro') #gainsboro
                    
FIXATION_CROSS = visual.TextStim(win,"+",color='black',height=0.4) # Define la cruz de fijacion
timer = core.Clock() 
# Instrucciones 
mensaje = 'En este experimento se le mostrarán secuencias de letras en rápida sucesión\nDentro de cada secuencia aparecerán dos números entre 2 y 9\nUna vez mostrada la secuencia, se le pedirá que identifique el primer y segundo número usando las teclas correspondientes a esos números\nEn los casos en los que usted no sienta haber visto un número, por favor intente adivinarlo\nPresione la barra espaciadora para iniciar una sesión de práctica del experimento'
MENSAJE = visual.TextStim(win,mensaje,color='black',wrapWidth=2)
MENSAJE.draw()
win.flip() 
event.waitKeys(keyList=['space'])  # Tecla para avanzar


# Presenta trials de practica
]
for trial in np.arange(len(practice_trials)): # itera sobre los trials de practica
    stream = practice_trials[trial] # define el stream correspondiente al trial
    FIXATION_TIME = randint(1000,1501)/1000  # la cruz de fijacion se muestra por un tiempo al azar entre 1 y 1.5 segundos
    FIXATION_CROSS.draw() # dibuja la cruz de fijacion
    win.flip() # avanza la pantalla
    core.wait(FIXATION_TIME) # espera el tiempo de fijacion
    for s in stream: # itera sobre el stream
        STIMULUS = visual.TextStim(win,s,color='black',height=0.4) # define el estimulo
        STIMULUS.draw() # dibuja el estimulo
        win.flip() # avanza la pantalla
        core.wait(0.1) # espera 0.1 s   Se puede reducir a 50 ms , por ejemplo, si es demasiado facil
        
    # Reporte de los targets   
    PREGUNTA1 = visual.TextStim(win,'Escriba con el teclado el primer número en la secuencia (entre 2 y 9):',color='black')
    PREGUNTA1.draw()
    win.flip()
    keys = event.waitKeys(keyList=['2','3','4','5','6','7','8','9']) # Respuesta sposibles
    
    if str(keys[0])== practice_targets[trial][0]: # Si la respuesta es correcta

        win.flip() 
        mensajecorrecto = 'Respuesta correcta! Presione la barra espaciadora para continuar'
        MENSAJE = visual.TextStim(win,mensajecorrecto,color='black')
        MENSAJE.draw()
        win.flip() 
        event.waitKeys(keyList=['space'])
        
    else: # Si la respuesta es incorrecta
        win.flip() 
        mensajeincorrecto = 'Respuesta incorrecta! Presione la barra espaciadora para continuar'
        MENSAJE = visual.TextStim(win,mensajeincorrecto,color='black')
        MENSAJE.draw()
        win.flip() 
        event.waitKeys(keyList=['space'])
        
    # Idem para el target 2
    PREGUNTA2 = visual.TextStim(win,'Escriba con el teclado el segundo número en la secuencia (entre 2 y 9):',color='black')
    PREGUNTA2.draw()
    win.flip()
    keys = event.waitKeys(keyList=['2','3','4','5','6','7','8','9'])
    
    if str(keys[0])== practice_targets[trial][1]:

        win.flip() 
        mensajecorrecto = 'Respuesta correcta! Presione la barra espaciadora para continuar'
        MENSAJE = visual.TextStim(win,mensajecorrecto,color='black')
        MENSAJE.draw()
        win.flip() 
        event.waitKeys(keyList=['space'])
        
    else:
        win.flip() 
        mensajeincorrecto = 'Respuesta incorrecta! Presione la barra espaciadora para continuar'
        MENSAJE = visual.TextStim(win,mensajeincorrecto,color='black')
        MENSAJE.draw()
        win.flip() 
        event.waitKeys(keyList=['space'])
        
# Fin de practica!
MENSAJE = visual.TextStim(win,'Sesión de práctica terminada! Si tiene dudas adicionales, por favor consulte con el experimentador a cargo\nPresione la barra espaciadora para empezar el experimento' ,color='black',wrapWidth=2)
MENSAJE.draw()
win.flip() 
event.waitKeys(keyList=['space'])

# Repite lo anterior pero para los trials del experimento "real" (NUMTRIALS)

respuestas_T1 = []
respuestas_T2 = []
correcto_T1 = []
correcto_T2 = []
reaction_time_T1 = []
reaction_time_T2 = []

for trial in np.arange(len(real_trials)):
    stream = real_trials[trial]
    FIXATION_TIME = randint(1000,1501)/1000
    FIXATION_CROSS.draw()
    win.flip()
    core.wait(FIXATION_TIME)
    marker = 0
    for s in stream:        
        STIMULUS = visual.TextStim(win,s,color='black',height=0.4)
        STIMULUS.draw()
        win.flip()
        core.wait(0.1) # se puede reducir a 50 ms en caso de que sea demasiado facil
   
    timer.reset()
    PREGUNTA1 = visual.TextStim(win,'Escriba con el teclado el primer número en la secuencia (entre 2 y 9):',color='black')
    PREGUNTA1.draw()
    win.flip()
    keys = event.waitKeys(keyList=['2','3','4','5','6','7','8','9'])
    resp_time = timer.getTime()
    reaction_time_T1.append(resp_time)
    respuestas_T1.append(str(keys[0]))
    if str(keys[0])== real_targets[trial][0]:
        correcto_T1.append(1) # Guarda un 1 si ese trial fue correcto para el target T1
        win.flip() 
        
        
    else:
        correcto_T1.append(0) # Guarda un 0 si ese trial fue correcto para el target T1
        win.flip() 
        
    timer.reset() 
    PREGUNTA2 = visual.TextStim(win,'Escriba con el teclado el segundo número en la secuencia (entre 2 y 9):',color='black')
    PREGUNTA2.draw()
    win.flip()
    keys = event.waitKeys(keyList=['2','3','4','5','6','7','8','9'])
    resp_time = timer.getTime()
    reaction_time_T2.append(resp_time)
    respuestas_T2.append(str(keys[0]))
    if str(keys[0])== real_targets[trial][1]:
        correcto_T2.append(1) # Guarda un 1 si ese trial fue correcto para el target T2
        win.flip() 
       
        
    else:
        correcto_T2.append(0) # Guarda un 0 si ese trial fue correcto para el target T2
        win.flip() 
       
        
MENSAJE = visual.TextStim(win,'Gracias por participar! Presione la barra espaciadora para terminar el experimento' ,color='black')
MENSAJE.draw()
win.flip() 
event.waitKeys(keyList=['space'])


print("Fin")

# Guarda los resultados en un archivo csv

T1s = []
T2s = []

for t in real_targets:
    T1s.append( t[0] )
    T2s.append( t[1] )
    
    
PosT1s = []
PosT2s = []

for t in real_positions:
    PosT1s.append( t[0] )
    PosT2s.append( t[1] )
    
data = {'Trial':np.arange(1,NUMTRIALS+1), 'T1':T1s, 'T2':T2s, 'Lag':real_lags, 'PosT1': PosT1s, 'PosT2': PosT2s, 'Respuesta T1':respuestas_T1,'Respuesta T2':respuestas_T2, 'Correcto T1':correcto_T1,'Correcto T2':correcto_T2, 'Reaction Time T1':reaction_time_T1, 'Reaction Time T2':reaction_time_T2} 
df = pd.DataFrame(data) 

df.to_csv(PARTICIPANT_FILENAME)

win.close()