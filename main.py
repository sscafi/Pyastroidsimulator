import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

# Set up the GUI
root = tk.Tk()
root.title("Object Fall Simulation")

# Create input fields for user
altitude_label = tk.Label(root, text="Initial Altitude (m):")
altitude_label.pack()
altitude_entry = tk.Entry(root)
altitude_entry.pack()

velocity_label = tk.Label(root, text="Initial Velocity (m/s):")
velocity_label.pack()
velocity_entry = tk.Entry(root)
velocity_entry.pack()

angle_label = tk.Label(root, text="Initial Angle (degrees):")
angle_label.pack()
angle_entry = tk.Entry(root)
angle_entry.pack()

# Create a function to simulate the object's fall
def simulate_fall():
    try:
        # Get user input
        altitude = float(altitude_entry.get())
        velocity = float(velocity_entry.get())
        angle = float(angle_entry.get())

        # Convert angle to radians
        angle_rad = math.radians(angle)

        # Calculate the object's initial x and y velocities
        vx = velocity * math.cos(angle_rad)
        vy = velocity * math.sin(angle_rad)

        # Simulate the object's fall
        time = 0
        dt = 0.01
        x = 0
        y = altitude
        vx_list = [vx]
        vy_list = [vy]
        x_list = [x]
        y_list = [y]
        t_list = [time]

        while y > 0:
            # Calculate the object's new position
            x += vx * dt
            y -= vy * dt

            # Calculate the object's new velocity
            vy -= 9.8 * dt  # gravity
            vx -= 0.1 * vx * dt  # atmospheric resistance
            vy -= 0.05 * vy * dt  # wind resistance

            # Update the lists
            vx_list.append(vx)
            vy_list.append(vy)
            x_list.append(x)
            y_list.append(y)
            t_list.append(time)

            # Update the time
            time += dt

        # Create a 3D plot of the object's trajectory
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x_list, np.zeros(len(x_list)), y_list, 'b-')

        # Add a 3D representation of the Earth
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x_earth = 6371 * np.outer(np.cos(u), np.sin(v))
        y_earth = 6371 * np.outer(np.sin(u), np.sin(v))
        z_earth = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x_earth, y_earth, z_earth, color='g', alpha=0.3)

        # Animate the object's trajectory
        def animate(i):
            ax.clear()
            ax.plot(x_list[:i], np.zeros(i), y_list[:i], 'b-')
            ax.plot_surface(x_earth, y_earth, z_earth, color='g', alpha=0.3)
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_zlabel('Z (m)')

        ani = animation.FuncAnimation(fig, animate, frames=len(x_list), interval=20)

        # Display the object's velocity and altitude in real-time
        def update_velocity_altitude(i):
            velocity_label.config(text=f"Velocity: {vx_list[i]:.2f} m/s")
            altitude_label.config(text=f"Altitude: {y_list[i]:.2f} m")

        for i in range(len(x_list)):
            update_velocity_altitude(i)
            root.update()
            root.after(20)

        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Invalid input")

# Create a button to start the simulation
start_button = tk.Button(root, text="Start Simulation", command=simulate_fall)
start_button.pack()

# Start the GUI event loop
root.mainloop()