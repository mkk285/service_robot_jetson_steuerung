import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tty
import termios
import sys
import threading
import time
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# Best Effort QoS Profil
best_effort_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE
)

# Tastenbelegung (WASD)
key_bindings = {
    'w': ( 0.5,  0.0),  # Vorwärts
    's': (-0.5,  0.0),  # Rückwärts
    'a': ( 0.0,  0.5),  # Drehung gegen UZS
    'd': ( 0.0, -0.5),  # Drehung im UZS
}

# Hilfe-Text
msg = """
Tastenbelegung (WASD):
       w
   a   s   d

w: Vorwärts
s: Rückwärts
a: Drehung links
d: Drehung rechts

Taste gedrückt halten zum Fahren.
Loslassen zum Stoppen.
Strg+C zum Beenden.
"""

class TeleopKeyNode(Node):
    def __init__(self):
        super().__init__('servicerobot_teleop_keyboard_node')
        self.publisher_ = self.create_publisher(
            Twist, 
            '/cmd_vel', 
            best_effort_qos
        )
        self.get_logger().info(msg)

        self.twist_ = Twist()
        self.last_key_time_ = time.time()
        self.timer_ = self.create_timer(0.02, self.timer_callback)
        self.settings_ = termios.tcgetattr(sys.stdin)

        self.key_thread_ = threading.Thread(target=self.key_loop)
        self.key_thread_.daemon = True
        self.key_thread_.start()

    def timer_callback(self):
        if (time.time() - self.last_key_time_) > 0.5:
            self.twist_.linear.x = 0.0
            self.twist_.angular.z = 0.0
        self.publisher_.publish(self.twist_)

    def key_loop(self):
        tty.setraw(sys.stdin.fileno())
        try:
            while rclpy.ok():
                key = sys.stdin.read(1)

                if key in key_bindings:
                    self.twist_.linear.x = key_bindings[key][0]
                    self.twist_.angular.z = key_bindings[key][1]
                    self.last_key_time_ = time.time()
                elif key == '\x03':
                    self.get_logger().info("Strg+C gedrückt, beende...")
                    rclpy.shutdown()
                    break
                else:
                    self.twist_.linear.x = 0.0
                    self.twist_.angular.z = 0.0
                    self.last_key_time_ = time.time()

        except Exception as e:
            if "EINTR" not in str(e):
                self.get_logger().error(f"Fehler im Tasten-Thread: {e}")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)

    def cleanup(self):
        stop_twist = Twist()
        self.publisher_.publish(stop_twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)
        self.get_logger().info("Terminal-Einstellungen wiederhergestellt.")

def main(args=None):
    rclpy.init(args=args)
    node = TeleopKeyNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass 
    except Exception as e:
        node.get_logger().error(f"Unerwarteter Fehler: {e}")
    finally:
        node.cleanup()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
