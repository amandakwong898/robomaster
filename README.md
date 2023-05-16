# Robomaster

**Team Members:** Amanda Kwong, Austin Guiney, Chirag Nagendra, Sanjana Nakhwa

**Team Leaders:** Amanda Kwong and Austin Guiney

**Project Overview:**

The goal of this project is to create a tag game with multiple RoboMaster S1 devices. One of the RoboMaster devices will act as a “guard” by patrolling an open area in a specific movement pattern. When the RoboMaster spots a target, it will transition into a “chase” state and hunt down the object that it has detected. When the fleeing object is out of sight, the RoboMaster will transition back to its “guard” state. 

Each robot will be equipped with functionalities such as tracking objects, voice commands, and event listeners. An offline simulation will be run to generate a list of instructions that the RoboMaster can execute. The software will spoof the RoboMaster app in order to overcome the built-in limitations of the hardware set by the manufacturer.

This project will employ post-processing techniques from RoboMaster data by recording video footage onto an SD card and using an external library to analyze and visualize data. 

**Project Requirements:**
1. Movement patterns: The RoboMaster should be able to move in specific patterns, resembling the way that a security guard patrols a shopping mall.
2. Object distance detection: The RoboMaster should be able to detect how far away an object is by using the focal length and DPI of its camera.
3. Clap detection: The RoboMaster should be able to respond to a clap, which will start or stop the game.
4. Collision avoidance: The RoboMaster should be able to avoid collisions with other objects by applying a “braking system” that deploys when it is close to colliding with another object.
5. Tagging feature: The RoboMaster should be able to “tag” other RoboMasters by firing a gel bead onto another RoboMaster’s motion detectors. This will cause the tagged RoboMaster to start hunting down the other RoboMasters.
6. Artificial intelligence: The RoboMaster should be able to make decisions on its own without input from the user.
7. RoboMaster simulation: An offline simulation will be run to generate a list of instructions that the RoboMaster can execute.
8. Instruction processing: The RoboMaster should be able to accept a list of instructions and execute them.
9. RoboMaster app spoofing: The RoboMaster app should be spoofed in order to gain new functionality.
10. Data visualization: Once data is gathered, we will post-process the data using visualizations that will display key metrics and insights to help users understand the relationships between variables and the outputs of the model.

**Project Directory**:

/prototypes/: This directory contains the prototypes for this project. See the [Project Wiki](https://github.com/amandakwong898/robomaster/wiki/Prototypes) for more information.

/tagging-game/: This directory contains files for the RoboMaster S1 tagging game.

/json-parsing/: This directory contains files for generating and parsing JSON strings for the RoboMaster S1.

/post-processing/: This directory contains files for post-processing recorded video footage from the RoboMaster S1.
