import matplotlib.pyplot as plt
import numpy as np

V_H2 = np.genfromtxt("Data/V_H2_data.csv", delimiter=",", skip_header=1)
V_O2 = np.genfromtxt("Data/V_O2_data.csv", delimiter=",", skip_header=1)
U = np.genfromtxt("Data/U_or_I_data.csv", delimiter=",", skip_header=1)

H2_speed = np.zeros((V_H2.shape[0]-1, V_H2.shape[1]))
H2_speed[:, 0] = V_H2[:-1, 0]
O2_speed = np.zeros((V_O2.shape[0]-1, V_O2.shape[1]))
O2_speed[:, 0] = V_O2[:-1, 0]

param_name = input(">> Enter the parameter name (d, I, pH, U): ")
param_table = {
    "d": np.array([19]),
    "I": np.array([1, 0.75, 0.5, 0.25]),
    "pH": np.array([13, 13.5]),
    "U": np.array([30, 20, 10, 5]),
}
param_values = param_table[param_name]


# Plot V H2 vs Time
plt.figure()
for i in range(1, V_H2[0].shape[0]):
    plt.plot(V_H2[:, 0], V_H2[:, i], label= param_name + " = " + str(param_values[i-1]), marker=".")

    for j in range(1, V_H2.shape[1]):
        H2_speed[:,j], _ = np.polyfit(V_H2[:, 0], V_H2[:, j], deg=1)

plt.legend()
plt.title(r"$V_{H_2}$")
plt.xlabel("Time (min)")
plt.ylabel("Volume (mL)")
plt.grid(alpha=0.5)
plt.savefig("Plots/V_H2.png")
plt.show()

# Plot V O2 vs Time
plt.figure()
for i in range(1, V_O2[0].shape[0]):
    plt.plot(V_O2[:, 0], V_O2[:, i], label=param_name + " = " + str(param_values[i-1]), marker=".")
    
    for j in range(1, V_O2.shape[1]):
        O2_speed[:,j], _ = np.polyfit(V_O2[:, 0], V_O2[:, j], deg=1)

plt.legend()
plt.title(r"$V_{O_2}$")
plt.xlabel("Time (min)")
plt.ylabel("Volume (mL)")
plt.grid(alpha=0.5)
plt.savefig("Plots/V_O2.png")
plt.show()

# Plot U vs Time
plt.figure()
for i in range(1, U[0].shape[0]):
    plt.plot(U[:, 0], U[:, i], label=param_name + " = " + str(param_values[i-1]), marker=".")

plt.legend()
plt.xlabel("Time (min)")

if param_name != "U":
    plt.title(r"$U$")
    plt.ylabel("Voltage (V)")
else:
    plt.title(r"$I$")
    plt.ylabel("Current (A)")

plt.grid(alpha=0.5)
plt.savefig("Plots/U.png")
plt.show()

# Plot H2 speed vs Time
plt.figure()
plt.plot(param_values, H2_speed[-1, 1:], marker=".")
plt.title(r"$V_{H_2}$ speed")
plt.xlabel(param_name)
plt.ylabel("Speed (mL/min)")
plt.grid(alpha=0.5)
plt.savefig("Plots/H2_speed.png")
plt.show()

# Plot O2 speed vs Time
plt.figure()
plt.plot(param_values, O2_speed[-1, 1:], marker=".")

plt.title(r"$V_{O_2}$ speed")
plt.xlabel(param_name)
plt.ylabel("Speed (mL/min)")
plt.grid(alpha=0.5)
plt.savefig("Plots/O2_speed.png")
plt.show()


# Plot Faraday efficiency vs Time

if param_name == "U":
    theorical_speed = np.copy(U)
    theorical_speed[:, 1:] = (24.05e3*60)*theorical_speed[:, 1:]/(2*96485) # mol/s -> mL/min
    theorical_speed = theorical_speed[:-1, :]
    farad_eff_H2 = np.zeros(theorical_speed.shape)
    farad_eff_H2[:, 0] = theorical_speed[:, 0]
    farad_eff_H2[:, 1:] = 100*H2_speed[:, 1:]/theorical_speed[:, 1:]

    farad_eff_O2 = np.zeros(theorical_speed.shape)
    farad_eff_O2[:, 0] = theorical_speed[:, 0]
    farad_eff_O2[:, 1:] = 100*O2_speed[:, 1:]/(theorical_speed[:, 1:]/2)

elif param_name == "I":
    theorical_speed = np.zeros(U.shape)
    theorical_speed[:, 1:] = (24.05e3*60)*np.tile(param_values, (U.shape[0], 1))/(2*96485) # mol/s -> mL/min
    theorical_speed[:, 0] = U[:, 0]
    theorical_speed = theorical_speed[:-1, :]
    farad_eff_H2 = np.zeros(theorical_speed.shape)
    farad_eff_H2[:, 0] = theorical_speed[:, 0]
    farad_eff_H2[:, 1:] = 100*H2_speed[:, 1:]/theorical_speed[:, 1:]

    farad_eff_O2 = np.zeros(theorical_speed.shape)
    farad_eff_O2[:, 0] = theorical_speed[:, 0]
    farad_eff_O2[:, 1:] = 100*O2_speed[:, 1:]/(theorical_speed[:, 1:]/2)
    
else:
    theorical_speed = np.ones(U.shape)
    theorical_speed[:, 1:] = (24.05e3*60)*theorical_speed[:,1:]/(2*96485)
    theorical_speed[:, 0] = U[:, 0]
    theorical_speed = theorical_speed[:-1, :]
    farad_eff_H2 = np.zeros(theorical_speed.shape)
    farad_eff_H2[:, 0] = theorical_speed[:, 0]
    farad_eff_H2[:, 1:] = 100*H2_speed[:, 1:]/theorical_speed[:, 1:]

    farad_eff_O2 = np.zeros(theorical_speed.shape)
    farad_eff_O2[:, 0] = theorical_speed[:, 0]
    farad_eff_O2[:, 1:] = 100*O2_speed[:, 1:]/(theorical_speed[:, 1:]/2)

plt.figure()
plt.plot(param_values, farad_eff_H2[-1,1:], marker=".")

plt.title(r"Faraday efficiency $H_2$")
plt.xlabel(param_name)
plt.ylabel(r"Faraday efficiency $H_2$(%)")
plt.grid(alpha=0.5)
plt.savefig("Plots/farad_eff_H2.png")
plt.show()

plt.figure()
plt.plot(param_values, farad_eff_O2[-1,1:], marker=".")

plt.title(r"Faraday efficiency $O_2$")
plt.xlabel(param_name)
plt.ylabel(r"Faraday efficiency $O_2$(%)")
plt.grid(alpha=0.5)
plt.savefig("Plots/farad_eff_O2.png")
plt.show()


# Plot energy efficiency vs Time
if param_name == "U" or param_name == "I":
    energy_consumption = np.copy(U)
    energy_consumption[0,1:] = param_values*U[0,1:]*U[0,0] # U*I*t or I*U*t
    for i in range(1, energy_consumption.shape[0]):
        energy_consumption[i, 1:] = energy_consumption[i-1, 1:] + param_values*U[i, 1:]*(U[i, 0] - U[i-1, 0])*60 # J
    
    energy_eff_H2 = np.zeros(energy_consumption.shape)
    energy_eff_H2[:, 0] = energy_consumption[:, 0]
    energy_eff_H2[:, 1:] = 100*((285.8/24.05)*V_H2[:, 1:])/ energy_consumption[:, 1:]

    energy_eff_O2 = np.zeros(energy_consumption.shape)
    energy_eff_O2[:, 0] = energy_consumption[:, 0]
    energy_eff_O2[:, 1:] = 100*((2*285.8/(2*24.05))*V_O2[:, 1:])/ energy_consumption[:, 1:]

else:
    energy_consumption = np.ones(U.shape)
    energy_consumption[:, 0] = U[:, 0]
    energy_consumption[0,1:] = 1*U[0,1:]*U[0,0] # 1A*U*t
    for i in range(1, energy_consumption.shape[0]):
        energy_consumption[i, 1:] = energy_consumption[i-1, 1:] + 1*U[i, 1:]*(U[i, 0] - U[i-1, 0])*60

    energy_eff_H2 = np.zeros(energy_consumption.shape)
    energy_eff_H2[:, 0] = energy_consumption[:, 0]
    energy_eff_H2[:, 1:] = 100*((285.8/24.05)*V_H2[:, 1:])/ energy_consumption[:, 1:]

    energy_eff_O2 = np.zeros(energy_consumption.shape)
    energy_eff_O2[:, 0] = energy_consumption[:, 0]
    energy_eff_O2[:, 1:] = 100*((2*285.8/(24.05))*V_O2[:, 1:])/ energy_consumption[:, 1:]


plt.figure()
plt.plot(param_values, energy_eff_H2[-1,1:], marker=".")
plt.title(r"Energy efficiency $H_2$")
plt.xlabel(param_name)
plt.ylabel(r"Energy efficiency $H_2$ (%)")
plt.grid(alpha=0.5)
plt.savefig("Plots/energy_eff_H2.png")
plt.show()

plt.figure()
plt.plot(param_values, energy_eff_O2[-1,1:], marker=".")
plt.title(r"Energy efficiency $O_2$")
plt.xlabel(param_name)
plt.ylabel(r"Energy efficiency $O_2$ (%)")
plt.grid(alpha=0.5)
plt.savefig("Plots/energy_eff_O2.png")
plt.show()
