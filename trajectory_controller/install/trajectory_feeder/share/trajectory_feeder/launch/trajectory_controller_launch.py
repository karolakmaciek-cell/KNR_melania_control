from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
        Node(
            package='trajectory_controller',
            executable='melania_trajectory.py',
            name='MelaniaTrajectory'
        ),
        Node(
            package='trajectory_controller',
            executable='trajectory_server.py',
            name='TrajectoryServer'
        ),
        
    ])
