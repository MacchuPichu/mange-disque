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
	sudo apt-get install samba samba-common-bin -y
Répondre par oui pour toutes les questions
	
	sudo smbpasswd -a pi

Modifier le ficheri smb.conf
	sudo nano /etc/samba/smb.conf
Pour donner accès au répertoire user :
	Sous ####### Authentication #######
Ajouter: 
	security = user

Sous #######  Share Definitions ####### 
Modifier: 
	read only = no
	
Redémarrer le service SAMBA
	sudo service smbd restart
	
	Tester de se connecter depuis un windows
	
## Installation de audacious
	sudo apt-get install audacious -y

## Installation de pico TTS
	wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
	wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
	sudo apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb -y

## Installation xdotool :  clavier en ligne de commande
	sudo apt-get install xdotool -y

## Brancher la carte NFC et les boutons


