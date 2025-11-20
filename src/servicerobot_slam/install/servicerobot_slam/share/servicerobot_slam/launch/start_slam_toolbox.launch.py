import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_share = get_package_share_directory("servicerobot_slam")
    slam_params = os.path.join(pkg_share, "config", "mapper.yaml")

    return LaunchDescription([

        # --- LIDAR Node ---
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            name='rplidar_node',
            output='screen'
        ),

        # --- Static TF: base_link -> base_scan ---
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_lidar_tf',
            arguments=[
                "0.096", "0.003", "0.288",    # x y z
                "0", "0", "0",                 # roll pitch yaw
                "base_link", "base_scan"
            ]
        ),

        # --- SLAM Toolbox ---
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[slam_params],
            output='screen'
        ),
    ])
