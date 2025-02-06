# dexarm_description

This package contains the URDF model, meshes, and associated configuration files for the DexArm robotic manipulator. It provides a detailed representation of the robot's physical and visual characteristics, enabling simulation and visualization within the ROS2 framework.

## Installation
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws/src
    git clone https://github.com/mounteverset/dexarm_description.git
    sudo apt update
    rosdep install --from-paths src --ignore-src -r -y

    cd ~/ros2_ws
    colcon build

    source ~/ros2_ws/install/setup.bash

For the **Usage Guidelines**, users typically want to know how to visualize the robot model in RViz or launch it in a simulation environment. Assuming the package includes a launch file for visualization, the instructions might look like this:

## Usage

To visualize the DexArm model in RViz:

  ros2 launch dexarm_description view_dexarm.launch.py

## File Structure

The package is organized as follows:

- **urdf/**: Contains the Xacro files defining the robot's URDF model.
- **meshes/**: Holds the 3D models (in formats like STL or DAE) used for visualization and collision detection.
- **launch/**: Includes launch files for starting various configurations of the robot in simulation or visualization tools.
- **config/**: Stores configuration files, such as joint limits or physical parameters.
- **package.xml** and **CMakeLists.txt**: Standard ROS2 package files containing metadata and build instructions.

## License

This package is licensed under the [BSD-3-Clause License](LICENSE). Please see the LICENSE file for more details.


