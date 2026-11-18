from machine import I2C, Pin
import time
from pca9685 import PCA9685


#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
#print([hex(a) for a in i2c.scan()])


# Réglages
PIN_SDA = 0
PIN_SCL = 1
ADRESSE_PCA = 0x40


# Modif Imène ----------------------------------------------------------------------------
# Les positions correspondent à l'ordre d'une cellule braille classique
CANAL_SERVO_1 = 4 # Haut Gauche
CANAL_SERVO_2 = 7 # Milieu Gauche
CANAL_SERVO_3 = 10 # Bas Gauche
CANAL_SERVO_4 = 13 # Haut Droit
CANAL_SERVO_5 = 15 # Milieu Droit
CANAL_SERVO_6 = 2 # Bas Droit


liste_servo = [CANAL_SERVO_1, CANAL_SERVO_2, CANAL_SERVO_3, CANAL_SERVO_4, CANAL_SERVO_5, CANAL_SERVO_6]


bouton = Pin(20, Pin.IN, Pin.PULL_DOWN) # Initialisation du bouton sur le GP20
# bouton.value() = 0 si on appuie, 1 si relaché


# A chaque lettre, on associe sa configuration sous forme de liste, où la position correspond au servomoteur associé [HG, MG, BG, HD, MD, BD]
# On met sous forme de liste, où la position correspond à la position de la lettre dans l'alphabet (1 -> A)
alphabet_braille = [[1,0,0,0,0,0], [1,1,0,0,0,0], [1,0,0,1,0,0], [1,0,0,1,1,0], [1,0,0,0,1,0], [1,1,0,1,0,0], [1,1,0,1,1,0], [1,1,0,0,1,0], [0,1,0,1,0,0], [0,1,0,1,1,0],
                  [1,0,1,0,0,0], [1,1,1,0,0,0], [1,0,1,1,0,0], [1,0,1,1,1,0], [1,0,1,0,1,0], [1,1,1,1,0,0], [1,1,1,1,1,0], [1,1,1,0,1,0], [0,1,1,1,0,0], [0,1,1,1,1,0],
                 [1,0,1,0,0,1], [1,1,1,0,0,1], [0,1,0,1,1,1], [1,0,1,1,0,1], [1,0,1,1,1,1], [1,0,1,0,1,1]]


# Je voulais faire dictionnaire, mais inutile en fait. Je garde juste pour que ça soit plus simple pour nous, pour associer les listes et leur lettre.
# dict_alphabet = {'a':[1,0,0,0,0,0], 'b':[1,1,0,0,0,0], 'c':[1,0,0,1,0,0], 'd':[1,0,0,1,1,0], 'e':[1,0,0,0,1,0], 'f':[1,1,0,1,0,0], 'g':[1,1,0,1,1,0], 'h':[1,1,0,0,1,0], 'i':[0,1,0,1,0,0], 'j':[0,1,0,1,1,0],
#                   'k':[1,0,1,0,0,0], 'l':[1,1,1,0,0,0], 'm':[1,0,1,1,0,0], 'n':[1,0,1,1,1,0], 'o':[1,0,1,0,1,0], 'p':[1,1,1,1,0,0], 'q':[1,1,1,1,1,0], 'r':[1,1,1,0,1,0], 's':[0,1,1,1,0,0], 't':[0,1,1,1,1,0],
#                  'u':[1,0,1,0,0,1], 'v':[1,1,1,0,0,1], 'w':[0,1,0,1,1,1], 'x':[1,0,1,1,0,1], 'y':[1,0,1,1,1,1], 'z':[1,0,1,0,1,1]}


# ---------------------------------------------------------------------------------




FREQUENCE = 50 # Hz
MIN_US = 500 # impulsion pour 0°
MAX_US = 2500 # impulsion pour 180°
PAS = 5 # degrés par étape
PAUSE_MS = 30 # pause entre deux étapes


# Initialisation
i2c = I2C(0, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL), freq=100000)


adresses = i2c.scan()
print("Appareils I2C détectés :", [hex(a) for a in adresses])
#if ADRESSE_PCA not in adresses:
   # raise OSError("PCA9685 introuvable : vérifie SDA/SCL et l'alimentation")


pca = PCA9685(i2c, address=ADRESSE_PCA)
pca.freq(FREQUENCE) # indispensable : l'init de la classe ne règle pas la fréquence


# Conversion angle → position du servo
def set_servo_angle(canal, angle):
    angle = max(0, min(180, angle))
    us = MIN_US + (MAX_US - MIN_US) * angle / 180 # durée de l'impulsion en microsecondes
    periode_us = 1000000 / FREQUENCE # 20000 µs à 50 Hz
    ticks = int(us * 4096 / periode_us) # conversion en ticks (0-4095)
    pca.pwm(canal, 0, ticks) # le signal monte à 0 et redescend à "ticks"




def relacher_servo(canal):
    pca.duty(canal, 0) # coupe le signal : le servo ne force plus


# Modif Imène ----------------------------------------------------------------------------
def annonces_audio(nb):
    '''
    Fonction pour le retour audio.
    Prend en entrée un nombre allant de 0 à 27.
    Les nombres allant de 0 à 25 correspondent aux lettres.
    26 correspond à l'introduction.
    27 correspond à la conclusion.
    '''
    pass
# ---------------------------------------------------------------------------------


# Boucle de test
print("Si jamais ça part en cacahuètes, Ctrl+C pour couper le programme")
try:
#    while True:
#        for angle in range(0, 181, PAS):
#            set_servo_angle(CANAL_SERVO, angle)
#            time.sleep_ms(PAUSE_MS)
#        for angle in range(180, -1, -PAS):
#            set_servo_angle(CANAL_SERVO, angle)
#            time.sleep_ms(PAUSE_MS)


# Modif Imène ----------------------------------------------------------------------------
    indice_lettre = 0
    while True:
        if (indice_lettre == 26):
            # on a parcouru tout l'alphabet, on peut terminer l'apprentissage.
            # On annonce la phrase de conclusion
            annonces_audio(27) # fonction à compléter plus haut
            time.sleep_ms(PAUSE_MS)
            print("On a parcouru tous l'alphabet. Demander l'arrêt (? je sais pas comment ça fonctionne)")
            break


        # On appuie sur le bouton
        # ATTENTION: un problème serait la gestion du temps d'appui. Faire en sorte que plusieurs lettres ne se fassent pas en une seule fois si on appuie trop longtemps sur le bouton.
        # Normalement ça devrait aller si PAUSE_MS est assez grand je pense ?
        elif (bouton.value() == 0):
            # Possible gestion du temps d'appui, que un appui = une lettre


            # Si on appuie pour la première fois, on annonce la phrase d'introduction
            if (indice_lettre == 0) :
                annonces_audio(26) # fonction à compléter plus haut
           
            # On commence par baisser tous les picots (au cas ou si ce n'est pas déjà le cas)
            for i in range(6):
                set_servo_angle(liste_servo[i], 0)
            time.sleep_ms(PAUSE_MS)


            # On récupère la liste de la lettre en cours
            lettre_braille = alphabet_braille[indice_lettre]


            # On annonce une première fois la lettre obtenue, avant de lever les picots
            annonces_audio(indice_lettre) # fonction à compléter plus haut
            time.sleep_ms(PAUSE_MS)


            # On parcoure la liste de la lettre
            for i in range(6):
                # On lève les picots qui doivent être levé
                if (lettre_braille[i] == 1):
                    set_servo_angle(liste_servo[i], 180) # Je sais pas si c'est trop brusque
            # On ré-annonce la lettre en même temps que les picots
            annonces_audio(indice_lettre)
           
            # On incrémente pour passer à la prochaine lettre
            indice_lettre += 1
except KeyboardInterrupt:
    print("Arrêt demandé")
finally:
    for i in range(6):
        relacher_servo(liste_servo[i])
    print("Servos relâchés")
# ---------------------------------------------------------------------------------
