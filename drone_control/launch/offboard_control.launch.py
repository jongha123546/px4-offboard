"""
Launch file for off-board drone control on a companion computer over DDS
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals, LaunchConfigurationNotEquals
import socket

def generate_launch_description():

    return LaunchDescription([
        # Declare the hostname argument to adapt code to hardware it is running on
        # This checks if the code is running on the RPi with a hostname -> osprey
        DeclareLaunchArgument(
            name='RPi_hostname',
            default_value='osprey',
            description='Change code to run on RPi'
            ),
        # Start MicroXRCEAgent DDS if on the RPi that connects over serial (UART) to the Pixhawk FC
        ExecuteProcess(
                       condition=LaunchConfigurationEquals('RPi_hostname',socket.gethostname()),
                       cmd=[['echo \'osprey\' | sudo -S \
                           MicroXRCEAgent serial --dev /dev/ttyAMA0 -b 921600'
                           ]],
                       shell=True,
                      ),
        # With Gazebo SITL start MicroXRCEAgent DDS with udp connection (On your laptop)
        ExecuteProcess(
                       condition=LaunchConfigurationNotEquals('RPi_hostname',socket.gethostname()),
                       cmd=[[
                            'MicroXRCEAgent udp4 --port 8888 -v'
                           ]],
                       shell=True,
                      ),
        # Control node
        Node(
             package='drone_control',
             executable='drone_control',
             output='screen',
             shell=True,
            ),
        # Path planning node
        Node(
             package='drone_control',
             executable='path_planning',
             output='screen',
             shell=True,
            ),
    ])