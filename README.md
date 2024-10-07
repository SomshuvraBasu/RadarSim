# Radar Simulation Project

## Description
This project is a Python-based radar simulation that visualizes the operation of a sweeping radar system. It demonstrates the principles of radar detection, target tracking, and blip visualization in a dynamic, real-time environment. Implements realistic physics-based radar simulation with realistic target movement and detection.

https://github.com/user-attachments/assets/7e2bc9dd-b9da-41e0-b07a-7979d11aeb3f

## Features
- Realistic radar sweep simulation
- Dynamic target movement and detection
- Real-time blip updates based on radar sweeps
- Customizable radar and target parameters
- Visual representation of radar range, angles, and detected targets

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/radar-simulation.git
   ```
2. Install the required dependencies:
   ```
   pip install pygame
   ```

## Usage
Run the main simulation script:
```
python simulation.py
```

## File Structure
- `simulation.py`: Main script to run the radar simulation
- `radar.py`: Contains the Radar class with core radar functionality
- `objects.py`: Defines target objects like Aircraft and Ship

## Customization
You can adjust various parameters in the simulation:
- In `radar.py`: Modify radar properties like range, beam width, and sweep speed
- In `objects.py`: Adjust target properties such as speed, heading, and RCS
- In `simulation.py`: Change the number of targets or simulation window size

## Contributing
Contributions to improve the simulation or add new features are welcome. Please fork the repository and create a pull request with your changes.

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contact
For any questions or suggestions, please open an issue in the GitHub repository.
