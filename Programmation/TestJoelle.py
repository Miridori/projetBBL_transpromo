import struct # Sert à convertir les octets bruts du fichier en vrais nombres (ex: 16 bits)
from machine import I2C, Pin, PWM
import time
from pca9685 import PCA9685

# ------------------------------------------ 
# PARAMETRES 
# ------------------------------------------

# Pour l'audio 
PIN_AUDIO = 2
pwm = PWM(Pin(PIN_AUDIO))
pwm.freq(35000)

frequence_wav = 16000
delai_us = int(1_000_000 / frequence_wav)  # 125 µs entre chaque échantillon

PIN_SDA = 0
PIN_SCL = 1
ADRESSE_PCA = 0x40

CANAL_SERVO_1 = 4 # Haut Gauche
CANAL_SERVO_2 = 7 # Milieu Gauche
CANAL_SERVO_3 = 8 # Bas Gauche
CANAL_SERVO_4 = 10 # Haut Droit
CANAL_SERVO_5 = 13 # Milieu Droit
CANAL_SERVO_6 = 15 # Bas Droit
liste_servo = [CANAL_SERVO_1, CANAL_SERVO_2, CANAL_SERVO_3, CANAL_SERVO_4, CANAL_SERVO_5, CANAL_SERVO_6]

FREQUENCE = 50          # Hz
MIN_US = 500            # impulsion pour 0°
MAX_US = 2500           # impulsion pour 180°
ANGLE_BAS = 0
ANGLE_HAUT = 90         #### à changer pour voir quel angle fait monter le piston

PIN_BOUTON = 20

DELAI_SERVO = 300    # temps laissé à UN servo pour finir son mouvement
PAUSE_LETTRE = 1000  # temps pendant lequel la lettre reste affichée, on peut mettre plus longtemps, 2000 = 2sec

PIN_BOUTON = 4
# A modifier

# alphabet_braille = [[1,0,0,0,0,0], [1,1,0,0,0,0], [1,0,0,1,0,0], [1,0,0,1,1,0], [1,0,0,0,1,0], [1,1,0,1,0,0], [1,1,0,1,1,0], [1,1,0,0,1,0], [0,1,0,1,0,0], [0,1,0,1,1,0],
#                    [1,0,1,0,0,0], [1,1,1,0,0,0], [1,0,1,1,0,0], [1,0,1,1,1,0], [1,0,1,0,1,0], [1,1,1,1,0,0], [1,1,1,1,1,0], [1,1,1,0,1,0], [0,1,1,1,0,0], [0,1,1,1,1,0],
#                   [1,0,1,0,0,1], [1,1,1,0,0,1], [0,1,0,1,1,1], [1,0,1,1,0,1], [1,0,1,1,1,1], [1,0,1,0,1,1]]

alphabet_braille = {
    'a': ["A.wav", [1,0,0,0,0,0]], 'b': ["B.wav", [1,1,0,0,0,0]], 'c': ["C.wav", [1,0,0,1,0,0]],
    'd': ["D.wav", [1,0,0,1,1,0]], 'e': ["E.wav", [1,0,0,0,1,0]], 'f': ["F.wav", [1,1,0,1,0,0]],
    'g': ["G.wav", [1,1,0,1,1,0]], 'h': ["H.wav", [1,1,0,0,1,0]], 'i': ["I.wav", [0,1,0,1,0,0]],
    'j': ["J.wav", [0,1,0,1,1,0]], 'k': ["K.wav", [1,0,1,0,0,0]], 'l': ["L.wav", [1,1,1,0,0,0]],
    'm': ["M.wav", [1,0,1,1,0,0]], 'n': ["N.wav", [1,0,1,1,1,0]], 'o': ["O.wav", [1,0,1,0,1,0]],
    'p': ["P.wav", [1,1,1,1,0,0]], 'q': ["Q.wav", [1,1,1,1,1,0]], 'r': ["R.wav", [1,1,1,0,1,0]],
    's': ["S.wav", [0,1,1,1,0,0]], 't': ["T.wav", [0,1,1,1,1,0]], 'u': ["U.wav", [1,0,1,0,0,1]],
    'v': ["V.wav", [1,1,1,0,0,1]], 'w': ["W.wav", [0,1,0,1,1,1]], 'x': ["X.wav", [1,0,1,1,0,1]],
    'y': ["Y.wav", [1,0,1,1,1,1]], 'z': ["Z.wav", [1,0,1,0,1,1]]
}

alphabet_braille = {'a':["A.wav",[1,0,0,0,0,0]], 'b':["B.wav", [1,1,0,0,0,0]], 'c':["C.wav",[1,0,0,1,0,0]], 'd':["D.wav",[1,0,0,1,1,0]], 'e':["E.wav",[1,0,0,0,1,0]], 'f':["F.wav", [1,1,0,1,0,0]], 'g':["G.wav",[1,1,0,1,1,0]], 'h':["H.wav",[1,1,0,0,1,0]], 'i':["I.wav",[0,1,0,1,0,0]], 'j':["J.wav",[0,1,0,1,1,0]],
                  'k':["K.wav",[1,0,1,0,0,0]], 'l':["L.wav",[1,1,1,0,0,0]], 'm':["M.wav",[1,0,1,1,0,0]], 'n':["N.wav",[1,0,1,1,1,0]], 'o':["O.wav",[1,0,1,0,1,0]], 'p':["P.wav",[1,1,1,1,0,0]], 'q':["Q.wav",[1,1,1,1,1,0]], 'r':["R.wav",[1,1,1,0,1,0]], 's':["S.wav",[0,1,1,1,0,0]], 't':["T.wav",[0,1,1,1,1,0]],
                 'u':["U.wav",[1,0,1,0,0,1]], 'v':["V.wav",[1,1,1,0,0,1]], 'w':["W.wav", [0,1,0,1,1,1]], 'x':["X.wav", [1,0,1,1,0,1]], 'y':["Y.wav", [1,0,1,1,1,1]], 'z':["Z.wav",[1,0,1,0,1,1]]}


fichier_wav = "Bienvenue.wav"
# -----------------------------------
# Initialisation
# -----------------------------------
i2c = I2C(0, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL), freq=400000)
print("Appareils I2C détectés :", [hex(a) for a in i2c.scan()])

pca = PCA9685(i2c, address=ADRESSE_PCA)
pca.freq(FREQUENCE)

bouton = Pin(PIN_BOUTON, Pin.IN, Pin.PULL_DOWN)
etat_actuel = [1, 1, 1, 1, 1, 1]

# -----------------------------------
# Fonctions
# -----------------------------------

def set_servo_angle(canal, angle):
    angle = max(0, min(180, angle))
    us = MIN_US + (MAX_US - MIN_US) * angle / 180
    periode_us = 1000000 / FREQUENCE
    ticks = int(us * 4096 / periode_us)
    pca.pwm(canal, 0, ticks)

def relacher_servo(canal):
    pca.duty(canal, 0)
    
def audio(nom_fichier):
    chemin = "Alphabet_audio/" + nom_fichier
    try:
        with open(chemin, "rb") as f:
            f.seek(44)
            buf = bytearray(1024)
            duty = pwm.duty_u16
            ticks_us = time.ticks_us
            ticks_diff = time.ticks_diff
            unpack_from = struct.unpack_from

            while True:
                octets_lus = f.readinto(buf)
                if octets_lus == 0:
                    break
                t_suivant = ticks_us()
                for i in range(0, octets_lus - 1, 2):
                    valeur = unpack_from("<h", buf, i)[0] + 32768
                    duty(valeur)
                    t_suivant += delai_us
                    while ticks_diff(t_suivant, ticks_us()) > 0:
                        pass
        pwm.duty_u16(0) 
    except OSError:
        print("Fichier introuvable :", nom_fichier)
        
def afficher(config):
    # on baisse ceux qui doivent être baissé si jamais ils sont levéss
    for i in range(6):
        if etat_actuel[i] == 1 and config[i] == 0:
            set_servo_angle(liste_servo[i], ANGLE_BAS)
            etat_actuel[i] = 0 # on met à jour 
            time.sleep_ms(DELAI_SERVO)

    # l'inverse
    for i in range(6):
        if etat_actuel[i] == 0 and config[i] == 1:
            set_servo_angle(liste_servo[i], ANGLE_HAUT)
            etat_actuel[i] = 1 # on met à jour 
            time.sleep_ms(DELAI_SERVO)


# Test bouton
#     indice_lettre = 0
#     while True:
#         if bouton.value() == 0:
#             time.sleep_ms(30)
#             if bouton.value() == 0:
#                 while bouton.value() == 0:
#                     pass
#                 time.sleep_ms(30)
#                 
#                 print(indice_lettre)
#                 
#                 indice_lettre+=1


# -----------------------------------
# Programme principal
# -----------------------------------
print("Si jamais ça part en couilles, Ctrl+C pour couper le programme")
try:
    # Position de départ : tout baissé 
    for canal in liste_servo:
        set_servo_angle(canal, ANGLE_HAUT)
        time.sleep_ms(DELAI_SERVO)
        
    audio("Bienvenue.wav")


# DECOMMENTER POUR TESTER LE BOUTON 

#         # Attendre 10sec (avec un timer de 10 secondes). Si on appuie durant ce laps de temps, créer variable choix_aleatoire = False. Puis baisser tous les picots
#     choix_aleatoire = False # par défaut
#     depart = time.time()
#     arrive = time.time()

#    while arrive-depart < 10 : # on a mit 10 sec mais en vrai à voir
#         arrive = time.time()
#         if bouton.value() == 0:
#             time.sleep_ms(30)
#             if bouton.value() == 0:
#                 while bouton.value() == 0:
#                     pass
#                 time.sleep_ms(30)

#                 choix_aleatoire = True # on change l'état pour passer au mode aleatoire
#                 break

#     # on set le timer à 10 secondes
#     time.sleep_ms(10000)
#     if bouton.value() == 1:

    for i in range(26):
        lettre = chr(ord('a') + i)  
        fichier_audio, config = alphabet_braille[lettre] 
                     
        print("Lettre :", lettre.upper(), config)
        audio(fichier_audio)      
        afficher(config)
        time.sleep_ms(PAUSE_LETTRE)
        
    print("Alphabet terminé")
except KeyboardInterrupt:
    print("Arrêt demandé")
finally:
    for canal in liste_servo:
        set_servo_angle(canal, ANGLE_BAS)
        time.sleep_ms(DELAI_SERVO)
        relacher_servo(canal)
    print("Servos relâchés")
    