import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():
    rplidar_node = Node(
        package='rplidar_ros',
        executable='rplidar_node',  # alte Version
        name='rplidar_node',
        parameters=[{
            'serial_port': '/dev/rplidar',
            'serial_baudrate': 115200,
            'frame_id': 'base_scan',
            'inverted': False,
            'angle_compensate': True,
            'stop_motor_on_exit': True,
        }],
        output='screen'
    )

    tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_to_lidar_tf',
        arguments=[
            '--x', '0.096',
            '--y', '0.003',
            '--z', '0.288',
            '--yaw', '0', '--pitch','0', '--roll', '0',
            '--frame-id', 'base_link', 
            '--child-frame-id', 'base_scan'
        ],
        output='screen'
    )

    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[os.path.join(
            get_package_share_directory('servicerobot_slam'),
            'config',
            'mapper.yaml'
        )],
        output='screen'
    )

    # Event-Handler: Stoppt RPLidar beim Beenden
    stop_rplidar_on_exit = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=rplidar_node,
            on_exit=[Node(
                package='rplidar_ros',
                executable='rplidar_node',
                name='rplidar_stop',
                arguments=['--stop_motor'],
                output='screen'
            )]
        )
    )

    return LaunchDescription([
        rplidar_node,
        tf_node,
        slam_node,
        stop_rplidar_on_exit
    ])
