# magicmirror

1. Download
https://dl.armbian.com/orangepizeroplus2-h5/Ubuntu_xenial_next_nightly.7z

2. Flash using Etcher
https://etcher.io

3. Boot and login to console (from MacOS)

screen /dev/cu.usbmodem14231 115200

root / 1234

4. Set new root password

You are required to change your password immediately (root enforced)
Changing password for root.
(current) UNIX password:

5. Create a new user



| |_| |  __/| |  / /|  __/ | | (_) | |  __/| | |_| \__ \  / __/ 
 \___/|_|   |_| /____\___|_|  \___/  |_|   |_|\__,_|___/ |_____|
                                                                

Welcome to ARMBIAN 5.34.171121 nightly Ubuntu 16.04.3 LTS 4.13.14-sunxi64   
System load:   0.15 0.13 0.05   Up time:       2 min
Memory usage:  6 % of 482MB     IP:            
CPU temp:      48°C             
Usage of /:    8% of 15G    

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

6. Install LXDE

sudo apt-get update
sudo apt-get upgrade
apt-get install keyboard-configuration locales tzdata console-data task-lxde-desktop --install-recommends -f -y


