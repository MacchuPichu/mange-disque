#-- coding: utf-8--

import os       # On importe le module os pour lancer la ligne de commande
import time     # On importe le module time pour mettre en pause apres le lancment d'une commande
import threading
import datetime

import RPi.GPIO as GPIO

from rc522 import RFID

# UID en cours de lecture
uid_en_cours = "START_STOPPED"

# Volume par défaut
volume_au_demarrage = 75

# Stopper la lecture
stop_lecture = False

# On instancie la lib
rc522 = RFID() 

#Definition des pins
pin31 = 31 #(GPIO.BCM = 06)
pin32 = 32 #(GPIO.BCM = 12)
pin33 = 33 #(GPIO.BCM = 13)
pin35 = 35 #(GPIO.BCM = 19)
pin36 = 36 #(GPIO.BCM = 16)
pin37 = 37 #(GPIO.BCM = 26)
pin38 = 38 #(GPIO.BCM = 20)
pin40 = 40 #(GPIO.BCM = 21)
#GPIO.setmode(GPIO.BCM)
GPIO.setup(pin31, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin32, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin33, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin35, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin37, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin38, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pin40, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# repertoire de musique
music_folder = "/home/pi/Music/"

# lecteur = [0_nom_programme, 1_cmd_mise_en_route, 2_cmd_rew, 3_cmd_play_pause, 4_cmd_fwd]
vlc = ["vlc", " --play-and-exit ", ""]
audacious = ["audacious", " ", " --rew", " --play-pause", " --fwd", " --stop"]
lecteur_audio = audacious

class Tache(threading.Thread):
    # Thread chargé simplement de lancer une fonction asynchrone.

    def __init__(self, fonction):
        threading.Thread.__init__(self)
        self.fonction = fonction

    def run(self):
        while(True):
            # Code à exécuter pendant l'exécution du thread.
            self.fonction()
        
class Chansons(threading.Thread):

    # Thread chargé simplement de lancer une chanson (une songpath) dans la console.

    def __init__(self, songpath):
        threading.Thread.__init__(self)
        self.songpath = songpath

    def run(self):
        if self.songpath == "START_STOPPED" :
            logs("Lancement du lecteur " + lecteur_audio[0])
            os.system(lecteur_audio[0] + lecteur_audio[5])
        elif not self.songpath == "" :
            # Code à exécuter pendant l'exécution du thread.
            logs("Lecture '" + self.songpath + "' avec " + lecteur_audio[0])
            os.system(lecteur_audio[0] + lecteur_audio[1] + music_folder + "*" + self.songpath + "*")

def main():

    logs("Démarrage script")
    volume_default() 
    speech(music_folder, "Bonjour, choisissez ce que vous voulez écoutez !", True)
    #speech(music_folder, "Paul, Attention, derrière toi !", True)

    tache_nfc = Tache(scutation_nfc).start()
    tache_commande = Tache(scutation_commande).start()

def scutation_nfc():
    global uid_en_cours
    
    # Démarrage
    if uid_en_cours == "START_STOPPED" :
        Chansons(uid_en_cours).start()
        uid_en_cours = ""
        
    # Attente de détection d'uncode NFC
    uid = lecture_nfc(None)
    if not uid == "" and not uid == uid_en_cours:
        uid_en_cours = uid
        logs("Carte NFC détectée. UID : " + uid)
        check_existing_folder(uid)
        logs("Lancement lecture")
        Chansons(uid).start()
    time.sleep(1)

def scutation_commande():
    global stop_lecture
    
    if GPIO.input(pin31) == 0:
        volume(False)
    if GPIO.input(pin32) == 0:
        volume(True)
    if GPIO.input(pin33) == 0:
        logs("Arrêt du système")
        os.system("killall " + lecteur_audio[0])
        time.sleep(0.5)
        speech(music_folder, "Arrêt du système. à bientôt !", True)
        time.sleep(0.5)
        os.system("shutdown -h now")
        #os.system("reboot")
    if GPIO.input(pin35) == 0:
        logs("Envoi de la commande RANDOM")
        os.system("xdotool key ctrl+s")
    if GPIO.input(pin36) == 0:
        logs("Envoi de la commande REWIND")
        os.system("xdotool key alt+Up")
    if GPIO.input(pin37) == 0:
        logs("Envoi de la commande PLAY/PAUSE")
        os.system(lecteur_audio[0] + lecteur_audio[3])
    if GPIO.input(pin38) == 0:
        logs("Envoi de la commande FORWARD")
        os.system("xdotool key alt+Down")
    if GPIO.input(pin40) == 0 or stop_lecture:
        logs("Envoi de la commande STOP")
        os.system(lecteur_audio[0] + lecteur_audio[5])
        stop_lecture = False
    time.sleep(0.2)

def lecture_nfc(timeout):
    uid = ""
    if timeout is None:
        rc522.wait_for_tag()
    else: 
        rc522.wait_for_tag_with_timeout(timeout) # On attend qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() # Quand une puce a été lue, on récupère ses infos
    if not error : # Si on a pas d'erreur
        (error, uid_list) = rc522.anticoll() # On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
        if not error : # Si on a réussi à nettoyer
            uid = '.'.join([str(i) for i in uid_list]) 
    return uid
    
def focus_on_player():
    process = os.popen('xdotool search --name "audacious"')
    result = process.read()
    x = result.split("\n")
    for valeur in x:
        if len(valeur)>0:
            id = valeur
    process.close()
    os.system('xdotool windowfocus ' + id)

def check_existing_folder(uid):
    global stop_lecture

    # recherche d'un dossier contenant l'UID
    finded_uid = False
    dirs = os.listdir(music_folder)
    for file in dirs:
        if uid in file:
            finded_uid = True

    #Si non trouve, on creer le repertoire avec un wav qui demande d'ajouter des fichiers audios
    repertoire = music_folder + uid
    if not finded_uid:
        stop_lecture = True
        time.sleep(0.1)
        logs("Création du répertoire : " + repertoire)
        os.makedirs(repertoire)
        logs("    A présent, Vous pouvez copier du contenu dans le répertoire : " + repertoire)
        speech(repertoire, "La carte " + uid.replace(".",", ") + " n'es pas encore connu", True)
        speech(repertoire, "J'ai donc créé un nouveau répertoire", True)
        speech(repertoire, "je vous invite à copier de la musique a l'intérieur du répertoire " + uid.replace(".",", "), False)

def speech(repertoire, text, play_wav):
    os.system('pico2wave -l fr-FR -w '+repertoire+'/speech.wav "' +  text + '"')
    if play_wav:
        os.system('aplay '+repertoire+'/speech.wav')

def logs(texte):
    print("["+str(datetime.datetime.now())+"] - " + texte)

def volume(up):
    process = os.popen('amixer sget "PCM" | grep "Mono:"')
    result = process.read()
    x = result.split(" ")
    process.close()
    volume = int(x[5][1:len(x[5])-2])
    if up and volume<100:
        new_volume = volume+1
        print("Augmentation de "+ str(volume) + "% vers " + str(new_volume) + "%")
        os.system("amixer sset 'PCM' "+str(new_volume)+"%")
    elif not up and volume>0:
        new_volume = volume-1
        print("Diminution de "+ str(volume) + "% vers " + str(new_volume) + "%")
        os.system("amixer sset 'PCM' "+str(new_volume)+"%")
    
def volume_default():
    os.system("amixer sset 'PCM' "+str(volume_au_demarrage)+"%")  

main()
