# magicmirror

1. Download
Armbian_5.34.171119_Orangepizeroplus2-h5_Ubuntu_xenial_next_4.13.13
from armbian.com

2. Flash using Etcher
https://etcher.io

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

  ___  ____  _   _____                ____  _             ____  
 / _ \|  _ \(_) |__  /___ _ __ ___   |  _ \| |_   _ ___  |___ \ 
| | | | |_) | |   / // _ \ '__/ _ \  | |_) | | | | / __|   __) |
| |_| |  __/| |  / /|  __/ | | (_) | |  __/| | |_| \__ \  / __/ 
 \___/|_|   |_| /____\___|_|  \___/  |_|   |_|\__,_|___/ |_____|
                                                                

Welcome to ARMBIAN 5.34.171121 nightly Ubuntu 16.04.3 LTS 4.13.14-sunxi64   
System load:   0.19 0.05 0.02   Up time:       0 min
Memory usage:  6 % of 482MB     IP:            192.168.43.96
CPU temp:      62°C             
Usage of /:    10% of 15G    

New to Armbian? Check the documentation first: https://docs.armbian.com


You are using an Armbian nightly build meant only for developers to provide
constructive feedback to improve build system, OS settings or user experience.
If this does not apply to you, STOP NOW!. Especially don't use this image for
daily work since things might not work as expected or at all and may break
anytime with next update. YOU HAVE BEEN WARNED!

This image is provided AS IS with NO WARRANTY and NO END USER SUPPORT!.

Creating a new user account. Press <Ctrl-C> to abort

Please provide a username (eg. your forename): ****

6. Enable Wi-Fi

nmtui

Activate a connection->Choose network->Activate->Enter Wi-Fi password->Quit

6. Update system 
apt update
apt upgrade

7. Install chromium
apt install chromium-browser

8. Install XFCE

apt -y install xorg lightdm xfce4 tango-icon-theme gnome-icon-theme lightdm-gtk-greeter

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

9. Autostart XFCE

systemctl set-default graphical.target

(run systemctl set-default multi-user.target to return to console login
and then startxfce4 after login)


10. NodeJS

curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

apt install -y nodejs

11. Magic Mirror
apt install libgconf-2-4

git clone https://github.com/stacywebb/magicmirror_arm64

cd /root/magicmirror_arm64

npm install

cp config/config.js.sample config/config.js

cd vendor
npm install
cd ..

npm start
