#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyControl(Node):
    def __init__(self):
        super().__init__('joy_control')
        
        # Publisher & Subscriber
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # TIMER: 10 Hz (0.1 Sekunden)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Einstellungen & Tasten (LED AUS = Analog)
        self.max_linear_vel = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.max_angular_vel = 0.75
        self.vel_index = 0
        self.axis_linear = 1
        self.axis_angular = 3
        self.btn_inc = 1
        self.btn_dec = 2

        # Speicher für Werte
        self.current_linear = 0.0
        self.current_angular = 0.0
        
        self.get_logger().info("JoyControl (10 HZ CLEAN) gestartet.")

    def joy_callback(self, msg):
        # Speed Logik
        if msg.buttons[self.btn_inc] == 1 and self.vel_index < 9:
            self.vel_index = min(self.vel_index + 1, 9)
            self.get_logger().info(f"Speed UP: {self.vel_index}")
        elif msg.buttons[self.btn_dec] == 1 and self.vel_index > 0:
            self.vel_index = max(self.vel_index - 1, 0)
            self.get_logger().info(f"Speed DOWN: {self.vel_index}")

        # WERTE NUR MERKEN (NICHT SENDEN!)
        self.current_linear = msg.axes[self.axis_linear]
        self.current_angular = msg.axes[self.axis_angular]

    def timer_callback(self):
        # HIER WIRD GESENDET (Takt: 10Hz)
        vel = Twist()
        current_max = self.max_linear_vel[self.vel_index]
        
        vel.linear.x = current_max * self.current_linear
        vel.angular.z = self.max_angular_vel * self.current_angular

        self.publisher_.publish(vel)

def main(args=None):
    rclpy.init(args=args)
    node = JoyControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
