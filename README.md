# MagicMirror using OrangePI Zero Plus 2 H5 and WaveShare 3.5 inch IPS LCD

0. SPI LCD wiring

|    PIN	  |  OrangePI |   LCD   |
| ---------|:---------:| -------:|
| +5V		    |    2			   |   2     |
| GND		    |    6			   |   6     |
| LCD_RS	  |    18	    |   18    |
| LCD_SI	  |    19	    |   19    |
| RST		    |    22	    |   22    |
| LCD_SCK	 |    23     |   23    |
| LCD_CS	  |    24     |   24    |

1. Download
https://dl.armbian.com/orangepizeroplus2-h5/Ubuntu_xenial_next.7z
from armbian.com

2. Flash using Etcher 
https://etcher.io 
or

rufus
http://rufus.akeo.ie/downloads/rufus-2.11p.exe

3. Boot and login to console (from MacOS)

screen /dev/cu.usbmodem14231 115200
or

screen /dev/cu.SLAB_USBtoUART 115200 
for CP2102 USB-UART 

root / 1234

4. Set new root password

You are required to change your password immediately (root enforced)
Changing password for root.
(current) UNIX password:

5. Create a new user

 ...

Creating a new user account. Press <Ctrl-C> to abort

Please provide a username (eg. your forename): magicmirror

6. Enable Wi-Fi

nmtui

Activate a connection->Choose network->Activate->Enter Wi-Fi password->Quit

7. Update system 
apt update
apt upgrade

8. Install display driver

nano /boot/armbianEnv.txt

replace 

overlays=usbhost2 usbhost3

to 

overlays=usbhost2 usbhost3 spi-spidev

add to the end

param_spidev_spi_bus=1


nano /etc/modules-load.d/fbtft.conf
fbtft
fbtft_device

nano /etc/modprobe.d/fbtft.conf

options fbtft_device name=piscreen gpios=dc:18,reset:2 speed=16000000 busnum=1 rotate=270 fps=30 bgr=1

apt install xserver-xorg-video-fbdev

nano /usr/share/X11/xorg.conf.d/99-fbdev.conf

Section "Device"  
  Identifier "myfb"
  Driver "fbdev"
  Option "fbdev" "/dev/fb0"
EndSection
 

9. Install XFCE

apt install xorg lightdm xfce4 lightdm-gtk-greeter

nano /etc/lightdm/lightdm.conf.d/11-armbian.conf

replace
[SeatDefaults]

to
[Seat:*]

replace
user-session=ubuntu

to
user-session=xfce

add to the end

autologin-user=magicmirror
autologin-user-timeout=0

nano /usr/share/lightdm/lightdm.conf.d/50-xserver-command.conf

replace 
xserver-command=X -core

to
xserver-command=X -bs -core -nocursor


10. Install chromium
apt install chromium-browser

11. NodeJS

curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -

apt install -y nodejs

12. Install MagicMirror
apt install libgconf-2-4

Login as magicmirror

git clone https://github.com/stacywebb/magicmirror_arm64

mv magicmirror_arm64 MagicMirror/

cd MagicMirror

nano package.json

replace 

 "chromedriver": "^2.33.1",
 
 to 
 
  "chromedriver": "2.33.1",

npm install

cp config/config.js.sample config/config.js

cd vendor
npm install
cd ..

npm start

13. Autostart MagicMirror

nano /home/magicmirror/mm.sh

add
cd ~/MagicMirror
DISPLAY=:0 npm start

chmod +x mm.sh

In XFCE Applications->Settings->Session and Startup->Application Autostart->Add

Name: Magic Mirror
Command: /home/magicmirror/mm.sh

Press OK

14. TightVNC

apt install tightvncserver

Start
tightvncserver :1 -geometry 800x480 -dpi 96 -nolisten tcp

Stop
tightvncserver -kill :1

Connect
http://www.tightvnc.com/download.php

ipaddress:5901

15. Mosquitto

apt install mosquitto

/etc/init.d/mosquitto start

mosquitto_passwd -c /etc/mosquitto/passwd smhome
Password:

nano /etc/mosquitto/conf.d/default.conf
add

allow_anonymous false
password_file /etc/mosquitto/passwd


systemctl restart mosquitto

16. Node-red

npm install -g --unsafe-perm node-red

npm install -g pm2
pm2 start /usr/bin/node-red
pm2 save
pm2 startup

npm install -g --unsafe-perm node-red-admin

node-red-admin hash-pw

nano /root/.node-red/settings.js

replace


//adminAuth: {
//    type: "credentials",
//    users: [{
//        username: "admin",
//        password: "$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6tl8sJogENOMcx$
//        permissions: "*"
//    }]
//},


to 

adminAuth: {
    type: "credentials",
    users: [{
        username: "admin",
        password: "PW_HASH_HERE",
        permissions: "*"
    }]
} 

15. Open Node-Red dashboard
http://192.168.43.253:1880

and enter login / password
