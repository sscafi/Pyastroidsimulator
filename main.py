import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib import cm

class AsteroidSimulator:
    def __init__(self):
        # Set up the main window
        self.root = tk.Tk()
        self.root.title("Asteroid Impact Simulator")
        self.root.geometry("400x600")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', background='#2c3e50', foreground='white')
        style.configure('TEntry', background='#34495e')
        style.configure('TButton', background='#3498db', foreground='white')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input fields with validation
        self.create_input_field(main_frame, "Initial Altitude (km):", "altitude", 100)
        self.create_input_field(main_frame, "Initial Velocity (km/s):", "velocity", 20)
        self.create_input_field(main_frame, "Entry Angle (degrees):", "angle", 45)
        self.create_input_field(main_frame, "Asteroid Diameter (m):", "diameter", 10)
        
        # Create start button
        start_button = ttk.Button(main_frame, text="Start Simulation", command=self.simulate_fall)
        start_button.pack(pady=20)
        
        # Status labels
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=10)
        self.velocity_label = ttk.Label(self.status_frame, text="Current Velocity: 0 km/s")
        self.velocity_label.pack()
        self.altitude_label = ttk.Label(self.status_frame, text="Current Altitude: 0 km")
        self.altitude_label.pack()
        self.energy_label = ttk.Label(self.status_frame, text="Kinetic Energy: 0 MT")
        self.energy_label.pack()

    def create_input_field(self, parent, label_text, name, default):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = ttk.Entry(frame, width=15)
        entry.pack(side=tk.RIGHT)
        entry.insert(0, str(default))
        setattr(self, f"{name}_entry", entry)

    def calculate_atmospheric_density(self, altitude):
        # Simplified exponential atmospheric density model
        h = altitude * 1000  # Convert to meters
        rho0 = 1.225  # Sea level density (kg/m³)
        H = 7400  # Scale height (m)
        return rho0 * np.exp(-h / H)

    def calculate_drag_coefficient(self, velocity):
        # Mach number dependent drag coefficient
        mach = velocity / 343  # Speed of sound at sea level
        if mach < 1:
            return 0.47
        else:
            return 0.47 + 0.53 * (1 - np.exp(-(mach - 1)))

    def simulate_fall(self):
        try:
            # Get input values
            altitude = float(self.altitude_entry.get())
            velocity = float(self.velocity_entry.get())
            angle = float(self.angle_entry.get())
            diameter = float(self.diameter_entry.get())
            
            # Convert units and initialize parameters
            velocity *= 1000  # km/s to m/s
            altitude *= 1000  # km to m
            angle_rad = math.radians(angle)
            mass = math.pi * (diameter/2)**3 * 4/3 * 3000  # Assuming density of 3000 kg/m³
            area = math.pi * (diameter/2)**2
            
            # Initialize simulation arrays
            dt = 0.1
            time = 0
            x, y, z = 0, 0, altitude
            vx = velocity * math.cos(angle_rad)
            vy = 0
            vz = -velocity * math.sin(angle_rad)
            
            positions = [[x, y, z]]
            velocities = [[vx, vy, vz]]
            times = [time]
            
            # Main simulation loop
            while z > 0:
                # Current velocity magnitude
                v = math.sqrt(vx**2 + vy**2 + vz**2)
                
                # Atmospheric calculations
                rho = self.calculate_atmospheric_density(z/1000)
                cd = self.calculate_drag_coefficient(v)
                
                # Forces
                drag = 0.5 * rho * cd * area * v**2
                fx = -drag * vx/v
                fy = -drag * vy/v
                fz = -drag * vz/v - mass * 9.81
                
                # Update velocities
                vx += (fx/mass) * dt
                vy += (fy/mass) * dt
                vz += (fz/mass) * dt
                
                # Update positions
                x += vx * dt
                y += vy * dt
                z += vz * dt
                
                # Store values
                positions.append([x, y, z])
                velocities.append([vx, vy, vz])
                times.append(time)
                time += dt

            # Create visualization
            self.create_3d_visualization(positions, velocities, times, diameter)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numerical values")

    def create_3d_visualization(self, positions, velocities, times, diameter):
        positions = np.array(positions)
        velocities = np.array(velocities)
        
        # Create figure
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create Earth
        radius = 6371000  # Earth's radius in meters
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot Earth with realistic texture
        earth = ax.plot_surface(x, y, z, cmap=cm.gist_earth, alpha=0.7)
        
        # Create atmosphere visualization
        atmosphere = ax.plot_surface(x*1.1, y*1.1, z*1.1, color='skyblue', alpha=0.1)
        
        # Animation function
        def animate(frame):
            ax.clear()
            
            # Plot Earth and atmosphere
            ax.plot_surface(x, y, z, cmap=cm.gist_earth, alpha=0.7)
            ax.plot_surface(x*1.1, y*1.1, z*1.1, color='skyblue', alpha=0.1)
            
            # Plot trajectory
            trajectory = ax.plot(positions[:frame, 0], 
                               positions[:frame, 1], 
                               positions[:frame, 2], 
                               'r-', alpha=0.5, label='Trajectory')
            
            # Plot asteroid
            asteroid = ax.scatter(positions[frame, 0],
                                positions[frame, 1],
                                positions[frame, 2],
                                color='red', s=100)
            
            # Calculate and show current velocity
            v = np.linalg.norm(velocities[frame])
            altitude = positions[frame, 2]
            energy = 0.5 * (math.pi * (diameter/2)**3 * 4/3 * 3000) * v**2 / 4.184e15  # Convert to megatons TNT
            
            # Update status labels
            self.velocity_label.config(text=f"Current Velocity: {v/1000:.2f} km/s")
            self.altitude_label.config(text=f"Current Altitude: {altitude/1000:.2f} km")
            self.energy_label.config(text=f"Kinetic Energy: {energy:.2f} MT")
            
            # Set labels and limits
            ax.set_xlabel('X (km)')
            ax.set_ylabel('Y (km)')
            ax.set_zlabel('Z (km)')
            
            # Set consistent scale
            max_range = np.array([positions[:,0].max()-positions[:,0].min(),
                                positions[:,1].max()-positions[:,1].min(),
                                positions[:,2].max()-positions[:,2].min()]).max() / 2.0
            mean_x = positions[:,0].mean()
            mean_y = positions[:,1].mean()
            mean_z = positions[:,2].mean()
            ax.set_xlim(mean_x - max_range, mean_x + max_range)
            ax.set_ylim(mean_y - max_range, mean_y + max_range)
            ax.set_zlim(mean_z - max_range, mean_z + max_range)
            
            ax.view_init(elev=20, azim=frame % 360)
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(positions),
                                     interval=50, blit=False)
        
        plt.show()

    def run(self):
        self.root.mainloop()

# Create and run the simulator
simulator = AsteroidSimulator()
simulator.run()
