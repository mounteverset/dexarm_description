from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch_ros.actions import Node
from launch.conditions import UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.substitutions.launch_configuration import LaunchConfiguration


ARGUMENTS = [
    DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='use_sim_time'
    ),
    DeclareLaunchArgument(
        "use_fake_hardware",
        default_value="true",
        description="Start robot with fake hardware mirroring command to its states.",
    ),
    DeclareLaunchArgument(
        "fake_sensor_commands",
        default_value="false",
        description="Enable fake command interfaces for sensors used for simple simulations. Used only if 'use_fake_hardware' parameter is true.",
    ),
]

def generate_launch_description():
    is_simulation = LaunchConfiguration("use_sim_time")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")

    pkg_robot_description = get_package_share_directory(
        'dexarm_description')

    controller_manager_launch = PathJoinSubstitution(
        [pkg_robot_description, 'launch', 'controller_manager.launch.py'])

    ld = LaunchDescription(ARGUMENTS)

    controller_manager_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([controller_manager_launch]),
        launch_arguments=[
            ('use_sim_time', is_simulation),
            ('use_fake_hardware', use_fake_hardware),
            ('fake_sensor_commands', fake_sensor_commands)],
        condition=UnlessCondition(is_simulation)
    )
    ld.add_action(controller_manager_launch_include)

    ld.add_action(
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=['-t:= joint_trajectory_controller', 'joint_state_broadcaster'],
            output="screen",
        )
    )

    joint_state_broadcaster_node = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )
    ld.add_action(joint_state_broadcaster_node)


    joint_trajectory_controller_spawner = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    # Delay creating the position trajectory controller until the joint_state_broadcast node has been started so that
    # the position trajectory controller can get the different TF frames from the broadcaster
    delay_position_trajectory_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_node,
            on_exit=[joint_trajectory_controller_spawner],
        )
    )
    ld.add_action(delay_position_trajectory_controller_spawner_after_joint_state_broadcaster_spawner)


    # velocity_controller_spawner = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'velocity_controller'],
    #     output='screen'
    # )

    # Delay creating the velocity controller until the joint_state_broadcast node has been started so that
    # the velocity controller can get the different TF frames from the broadcaster
    # delay_velocity_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=joint_state_broadcaster_node,
    #         on_exit=[velocity_controller_spawner],
    #     )
    # )
    # ld.add_action(delay_velocity_controller_spawner_after_joint_state_broadcaster_spawner)

    return ld