import struct # Sert à convertir les octets bruts du fichier en vrais nombres (ex: 16 bits)
import time
from machine import PWM, Pin

# 1. Configuration de la broche reliée au haut-parleur
PIN_AUDIO = 2
pwm = PWM(Pin(PIN_AUDIO))

# Fréquence porteuse PWM (62.5 kHz est idéal pour le Pico et inaudible)
# Définit la fréquence porteuse du PWM à 35 000 Hz (35 kHz).
pwm.freq(35000)

# 2. Paramètres exacts de votre fichier WAV
fichier_wav = "S.wav"
# il faut prendre un fichier wav, mono canal, et 16bits 


frequence_wav = 8000  # Correspond à Frequence : (8000,)
delai_us = int(1_000_000 / frequence_wav)  # 125 µs entre chaque échantillon

try:
    
    # Ouvre le fichier audio en mode lecture binaire (read binary)	
    with open(fichier_wav, "rb") as f:
        # Sauter l'en-tête standard de 44 octets du fichier WAV
        f.seek(44)
        print("Lecture en cours...")
        
        # Crée une petite mémoire tampon (buffer) de 1024 octets.
        buf = bytearray(1024)  # 1024 octets = 512 échantillons de 16 bits
        
    
        # accélère énormément l'exécution à l'intérieur d'une boucle rapide.
        duty = pwm.duty_u16
        ticks_us = time.ticks_us
        ticks_diff = time.ticks_diff
        unpack_from = struct.unpack_from

# Boucle principale, lit le fichier 
        while True:
            octets_lus = f.readinto(buf)
            if octets_lus == 0:
                break

            t_suivant = ticks_us()
            # Avancer de 2 en 2 octets (car 16 bits = 2 octets par échantillon)
            for i in range(0, octets_lus - 1, 2):
                # Lire l'entier signé 16-bit (-32768 à +32767) et décaler en positif (0 à 65535)
                valeur = unpack_from("<h", buf, i)[0] + 32768
                duty(valeur)

# on attend juste la fin du délai
                t_suivant += delai_us
                while ticks_diff(t_suivant, ticks_us()) > 0:
                    pass

    print("Lecture terminée.")

except Exception as e:
    print("Erreur :", e)

# nettoie 
finally:
    pwm.duty_u16(0) # Met le signal PWM à 0 (silence total) pour éviter que le haut-parleur ne grésille ou ne chauffe
    pwm.deinit()    # Désactive complètement le module PWM sur la broche GP2 pour libérer la ressource
