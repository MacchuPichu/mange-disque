# mange-disque

## Préparation de la carte
Etcher
Raspbian desktop

## 1ier démarrage
HDMI(sur écran) + clavier/souris + alim
Suivre la 1iere installation, les mise à jour et configurer le Wifi

Apres redémarrage, Menu Configuration du Raspberry Pi
Dans l'onglet Interfaces, activer SSH, VNC, SPI, I2C

Récupérer l'adresse IP.
On peux se débrancher de l'écran, du clavier/souris et se connecter avec VNC

## Installation de samba
	
```bash
sudo apt-get install samba samba-common-bin -y
```

Répondre par oui pour toutes les questions
```bash
sudo smbpasswd -a pi
```
Modifier le ficheri smb.conf
```bash
sudo nano /etc/samba/smb.conf
```
Pour donner accès au répertoire user :
Sous ####### Authentication #######
Ajouter: 
```bash
security = user
```

Sous #######  Share Definitions ####### 
Modifier: 
```bash
read only = yes --> read only = no
```

Redémarrer le service SAMBA
```bash
sudo service smbd restart
```
Tester de se connecter depuis un windows
	
## Installation de audacious
```bash
sudo apt-get install audacious -y
```


## Installation de pico TTS
```bash
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
sudo apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb -y
```

## Installation xdotool :  clavier en ligne de commande
```bash
sudo apt-get install xdotool -y
```


## Brancher la carte NFC et les boutons

## Récupération du code source
```bash
git clone https://github.com/MacchuPichu/mange-disque.git /home/pi/Music/mange-disque
```
	

## Lancer le script au démarrage en mode LXDE
Rendre le script executable : 
```bash
sudo chmod +x /home/pi/Music/mange-disque/mange-disque.py
```
	

Ajouter la commande de lancement dans autostart
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
A la fin ajouter: 
```bash
@lxterminal -e /usr/bin/python3 /home/pi/Music/mange-disque/mange-disque.py
```


Ajouter les outils Bluetooth
```bash
sudo apt-get install blueman pulseaudio pavucontrol pulseaudio-module-bluetooth
```

