#!/bin/bash
# 1. Alle alten Instanzen radikal beenden
pkill -f joy_node
pkill -f joy_control_node
sleep 1

# 2. Umgebung laden
source /opt/ros/humble/setup.bash
source /home/jetson/robot_ws/install/setup.bash

# 3. Variablen (ID 42 wie heute konfiguriert)
export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# 4. Nodes im Hintergrund starten (Output unterdrücken für SSH-Stabilität)
ros2 run joy joy_node --ros-args -p device_id:=0 -p autorepeat_rate:=20.0 > /dev/null 2>&1 &
sleep 2
ros2 run servicerobot_joy joy_control_node.py > /dev/null 2>&1 &

echo "Joystick-Nodes wurden frisch gestartet."
