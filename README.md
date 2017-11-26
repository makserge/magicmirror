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
apt install chromium-browser

9 Install XFCE

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

10. Autostart XFCE

systemctl set-default graphical.target

(run systemctl set-default multi-user.target to return to console login
and then startxfce4 after login)

11. Set screen rotation
Applications->Settings->Display->Rotation->Left->Apply

11. NodeJS

curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

apt install -y nodejs

12. MagicMirror
apt install libgconf-2-4

git clone https://github.com/stacywebb/magicmirror_arm64

cd /root/magicmirror_arm64

npm install

cp config/config.js.sample config/config.js

cd vendor
npm install
cd ..

npm start

13. Autostart MagicMirror

mv magicmirror_arm64 /home/magicmirror/MagicMirror/

chown -R magicmirror.magicmirror /home/magicmirror/MagicMirror/

npm install -g pm2
pm2 startup

As magicmirror user:

cd /home/magicmirror

nano mm.sh

add
cd ~/MagicMirror
DISPLAY=:0 npm start

chmod +x mm.sh

In XFCE Applications->Settings->Session and Startup->Application Autostart->Add

Name: Magic Mirror
Command: /home/magicmirror/mm.sh

Press OK
