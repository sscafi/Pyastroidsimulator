# Asteroid Impact Simulator

A sophisticated 3D simulation tool for visualizing and analyzing asteroid atmospheric entry trajectories. This simulator provides real-time visualization of asteroid descent paths with accurate physics modeling and atmospheric interactions.

![Asteroid Simulator Screenshot](/api/placeholder/800/400)

## Features

* Real-time 3D visualization of asteroid trajectories
* Accurate atmospheric physics modeling
* Interactive parameter adjustment
* Kinetic energy calculations
* Altitude-dependent atmospheric density
* Mach number-dependent drag coefficients
* Realistic Earth and atmosphere visualization

## Installation

### Prerequisites

```bash
python >= 3.8
```

### Required Packages

```bash
numpy
matplotlib
tkinter
```

Install dependencies using pip:

```bash
pip install numpy matplotlib
```

Note: tkinter usually comes pre-installed with Python. If missing, install it using:

- On Ubuntu/Debian:
  ```bash
  sudo apt-get install python3-tk
  ```
- On Windows:
  ```bash
  python -m pip install tk
  ```

## Usage

1. Run the simulator:
   ```bash
   python asteroid_simulator.py
   ```

2. Input Parameters:
   - Initial Altitude (km): Starting height above Earth's surface
   - Initial Velocity (km/s): Entry velocity
   - Entry Angle (degrees): Angle relative to horizontal
   - Asteroid Diameter (m): Size of the asteroid

3. Click "Start Simulation" to begin the visualization

## Physics Model

### Atmospheric Density Model
The simulator uses an exponential atmospheric density model:
```python
ρ = ρ₀ * exp(-h/H)
```
where:
- ρ₀ = 1.225 kg/m³ (sea level density)
- H = 7400 m (scale height)
- h = altitude in meters

### Drag Coefficient
Mach number-dependent drag coefficient calculation:
```python
Cd = 0.47 + 0.53 * (1 - exp(-(M - 1)))  # for M > 1
Cd = 0.47                                # for M ≤ 1
```

### Energy Calculations
Kinetic energy is calculated and converted to megatons TNT:
```python
E = 0.5 * m * v² / 4.184e15  # MT TNT
```

## Features Breakdown

### Visual Components
- 3D Earth rendering with realistic texture
- Semi-transparent atmospheric layer
- Trajectory path with fade effect
- Real-time asteroid position
- Rotating camera view

### Real-time Metrics
- Current velocity (km/s)
- Current altitude (km)
- Kinetic energy (MT TNT)
- Trajectory visualization

### Physics Components
- Gravitational acceleration
- Atmospheric drag
- Variable density atmospheres
- Mass calculations
- Cross-sectional area effects

## Code Structure

```
AsteroidSimulator/
├── __init__.py
├── asteroid_simulator.py   # Main simulation code
└── README.md              # This file
```

### Main Class Structure
- `AsteroidSimulator`: Main class containing:
  - `__init__`: GUI initialization
  - `simulate_fall`: Physics calculations
  - `create_3d_visualization`: Visualization logic
  - `calculate_atmospheric_density`: Atmosphere model
  - `calculate_drag_coefficient`: Drag calculations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* Atmospheric density model based on the U.S. Standard Atmosphere
* Drag coefficient calculations inspired by aerospace research
* Visualization techniques using Matplotlib's 3D toolkit

## Version History

* 1.0.0
    * Initial Release
    * Basic trajectory simulation
    * 3D visualization
    * Real-time metrics

## Known Issues

* Frame rate may slow down with very long trajectories
* Limited to single-body physics (no fragmentation)
* Simplified atmospheric model

## Future Improvements

- [ ] Add ablation effects
- [ ] Implement asteroid fragmentation
- [ ] Add thermal effects
- [ ] Include more detailed atmospheric models
- [ ] Support for multiple simultaneous simulations
- [ ] Export simulation data to CSV
