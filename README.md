# MagicMirror using OrangePI Zero Plus 2 H5 and WaveShare 4 inch IPS LCD

1. Download
https://dl.armbian.com/orangepizeroplus2-h5/archive/Armbian_5.38_Orangepizeroplus2-h5_Debian_stretch_next_4.14.14.7z
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

8. Install chromium
apt install chromium

9 Install XFCE

apt install xorg lightdm xfce4 lightdm-gtk-greeter

nano /etc/lightdm/lightdm.conf.d/11-armbian.conf

add to the end

autologin-user=magicmirror
autologin-user-timeout=0

10. NodeJS

curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -

apt install -y nodejs

11. Install MagicMirror
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

12. Autostart MagicMirror

nano /home/magicmirror/mm.sh

add
cd ~/MagicMirror
DISPLAY=:0 npm start

chmod +x mm.sh

In XFCE Applications->Settings->Session and Startup->Application Autostart->Add

Name: Magic Mirror
Command: /home/magicmirror/mm.sh

Press OK

13. Mosquitto

apt install mosquitto

/etc/init.d/mosquitto start

mosquitto_passwd -c /etc/mosquitto/passwd smhome
Password:

nano /etc/mosquitto/conf.d/default.conf
add

allow_anonymous false
password_file /etc/mosquitto/passwd


systemctl restart mosquitto

14. Node-red

npm install -g --unsafe-perm node-red

npm install -g pm2
pm2 start /usr/bin/node-red
pm2 save
pm2 startup

npm install node-red-admin

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
