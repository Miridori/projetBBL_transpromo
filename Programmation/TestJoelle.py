from machine import I2C, Pin
import time
from pca9685 import PCA9685

# Réglages
PIN_SDA = 0
PIN_SCL = 1
ADRESSE_PCA = 0x40

#Les positions correspondent à l'ordre d'une cellule braille classique
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

DELAI_SERVO = 300    # temps laissé à UN servo pour finir son mouvement
PAUSE_LETTRE = 2000  # temps pendant lequel la lettre reste affichée, on peut mettre plus longtemps, 2000 = 2sec

alphabet_braille = [[1,0,0,0,0,0], [1,1,0,0,0,0], [1,0,0,1,0,0], [1,0,0,1,1,0], [1,0,0,0,1,0], [1,1,0,1,0,0], [1,1,0,1,1,0], [1,1,0,0,1,0], [0,1,0,1,0,0], [0,1,0,1,1,0],
                   [1,0,1,0,0,0], [1,1,1,0,0,0], [1,0,1,1,0,0], [1,0,1,1,1,0], [1,0,1,0,1,0], [1,1,1,1,0,0], [1,1,1,1,1,0], [1,1,1,0,1,0], [0,1,1,1,0,0], [0,1,1,1,1,0],
                  [1,0,1,0,0,1], [1,1,1,0,0,1], [0,1,0,1,1,1], [1,0,1,1,0,1], [1,0,1,1,1,1], [1,0,1,0,1,1]]

# alphabet_braille = {'a':[1,0,0,0,0,0], 'b':[1,1,0,0,0,0], 'c':[1,0,0,1,0,0], 'd':[1,0,0,1,1,0], 'e':[1,0,0,0,1,0], 'f':[1,1,0,1,0,0], 'g':[1,1,0,1,1,0], 'h':[1,1,0,0,1,0], 'i':[0,1,0,1,0,0], 'j':[0,1,0,1,1,0],
#                   'k':[1,0,1,0,0,0], 'l':[1,1,1,0,0,0], 'm':[1,0,1,1,0,0], 'n':[1,0,1,1,1,0], 'o':[1,0,1,0,1,0], 'p':[1,1,1,1,0,0], 'q':[1,1,1,1,1,0], 'r':[1,1,1,0,1,0], 's':[0,1,1,1,0,0], 't':[0,1,1,1,1,0],
#                  'u':[1,0,1,0,0,1], 'v':[1,1,1,0,0,1], 'w':[0,1,0,1,1,1], 'x':[1,0,1,1,0,1], 'y':[1,0,1,1,1,1], 'z':[1,0,1,0,1,1]}


# -----------------------------------
# Initialisation
# -----------------------------------
i2c = I2C(0, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL), freq=400000)
print("Appareils I2C détectés :", [hex(a) for a in i2c.scan()])

pca = PCA9685(i2c, address=ADRESSE_PCA)
pca.freq(FREQUENCE)

def set_servo_angle(canal, angle):
    angle = max(0, min(180, angle))
    us = MIN_US + (MAX_US - MIN_US) * angle / 180
    periode_us = 1000000 / FREQUENCE
    ticks = int(us * 4096 / periode_us)
    pca.pwm(canal, 0, ticks)

def relacher_servo(canal):
    pca.duty(canal, 0)

# -----------------------------------
# Affichage d'une lettre
# -----------------------------------
# etat_actuel[i] = 1 si le picot i est levé, 0 sinon
# par ex afficher([1,0,0,0,0,0])
etat_actuel = [0, 0, 0, 0, 0, 0] # à mettre sur 1


# amélioration : ajouter le bouton, le passage entre chaque lettre se fait quand on clique sur le bouton 
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

# Programme principal
print("Si jamais ça part en couilles, Ctrl+C pour couper le programme")
try:
    # Position de départ : tout baissé 
    for canal in liste_servo:
        set_servo_angle(canal, ANGLE_BAS)
        time.sleep_ms(DELAI_SERVO)

# chr(ord('A') : ca donne les lettres de l'alphabet dans l'ordre
    for indice, config in enumerate(alphabet_braille):
        print("Lettre :", chr(ord('A') + indice), config)
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
    