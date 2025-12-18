#!/bin/bash

# --- KONFIGURATION ---
PI_USER="pi-motor"
PI_IP="192.168.0.114"  # Deine IP ist hier schon eingetragen

echo "--- [1] Räume auf ---"
# Beendet alte Jetson-Prozesse
killall -9 rplidar_node joy_node 2>/dev/null
# Beendet alte Pi-Prozesse (Motor aus!)
ssh $PI_USER@$PI_IP "pkill -f md49" &

sleep 2

echo "--- [2] Lade Jetson Umgebung ---"
source /opt/ros/humble/setup.bash
# Falls du auf dem Jetson auch workspaces hast (z.B. für Lidar/Kamera):
# source ~/robot_ws/install/setup.bash 

# Netzwerk-Setup (Muss gleich sein wie auf dem Pi!)
export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

echo "--- [3] Starte Lidar (Lokal am Jetson) ---"
# HIER den Startbefehl für deinen Lidar eintragen (Beispiel):
# nohup ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 -p frame_id:=laser > /dev/null 2>&1 &

sleep 1

echo "--- [4] Starte Motor (Remote auf Pi) ---"
# Der Jetson befiehlt dem Pi, sein Skript zu starten
ssh $PI_USER@$PI_IP "nohup ~/start_motor.sh > /dev/null 2>&1 &"

echo "✅ Systemstart eingeleitet."
