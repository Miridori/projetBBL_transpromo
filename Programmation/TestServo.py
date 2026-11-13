from machine import I2C, Pin
import time
from pca9685 import PCA9685

from machine import I2C, Pin
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
print([hex(a) for a in i2c.scan()])

# Réglages
PIN_SDA = 4
PIN_SCL = 5
ADRESSE_PCA = 0x40
CANAL_SERVO = 11 # canal du servo que je teste
FREQUENCE = 50 # Hz
MIN_US = 1000 # impulsion pour 0°
MAX_US = 2000 # impulsion pour 180°
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


# Boucle de test
print("Si jamais ça part en couilles, Ctrl+C pour couper le programme")
try:
    while True:
        for angle in range(0, 181, PAS):
            set_servo_angle(CANAL_SERVO, angle)
            time.sleep_ms(PAUSE_MS)
        for angle in range(180, -1, -PAS):
            set_servo_angle(CANAL_SERVO, angle)
            time.sleep_ms(PAUSE_MS)
except KeyboardInterrupt:
    print("Arrêt demandé")
finally:
    relacher_servo(CANAL_SERVO)
    print("Servo relâché")
