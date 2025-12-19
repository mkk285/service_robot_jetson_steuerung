#!/bin/bash

# Log-Datei erstellen (Damit wir sehen, was passiert)
LOGFILE=~/joystick_debug.log
echo "--- Neuer Start: $(date) ---" > $LOGFILE

# Umgebung laden
source /opt/ros/humble/setup.bash
source ~/robot_ws/install/setup.bash
export ROS_DOMAIN_ID=42

# 1. Aufräumen (Gezielt die Nodes töten, nicht das Skript selbst!)
# Wir nutzen pkill -x für exakte Treffer oder -f für Pfade
echo "Beende alte Prozesse..." >> $LOGFILE
pkill -f joy_linux_node
pkill -f joy_control
# Zur Sicherheit kurz warten
sleep 1

# 2. Treiber starten (joy_linux)
# Wir leiten die Ausgabe (>>) in die Logdatei um
echo "Starte joy_linux_node..." >> $LOGFILE
ros2 run joy_linux joy_linux_node --ros-args -p dev:="/dev/input/js0" -p autorepeat_rate:=20.0 >> $LOGFILE 2>&1 &

sleep 2

# 3. Steuerung starten
echo "Starte joy_control..." >> $LOGFILE
ros2 run servicerobot_joy joy_control >> $LOGFILE 2>&1 &

echo "Fertig. Nodes laufen im Hintergrund." >> $LOGFILE
