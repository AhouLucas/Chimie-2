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
    "d": np.array([19, 15, 11, 7]),
    "I": np.array([1, 0.75, 0.5, 0.25]),
    "pH": np.array([13, 13.5, 14]),
    "U": np.array([30, 20, 10, 5]),
}
param_values = param_table[param_name]


# Plot V H2 vs Time
plt.figure()
for i in range(1, V_H2[0].shape[0]):
    plt.plot(V_H2[:, 0], V_H2[:, i], label= param_name + " = " + str(param_values[i-1]))
    for j in range(V_H2.shape[0]-1):
        H2_speed[j, i] = (V_H2[j+1, i] - V_H2[j, i])/(V_H2[j+1, 0] - V_H2[j, 0])

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
    plt.plot(V_O2[:, 0], V_O2[:, i], label=param_name + " = " + str(param_values[i-1]))
    for j in range(V_O2.shape[0]-1):
        O2_speed[j, i] = (V_O2[j+1, i] - V_O2[j, i])/(V_O2[j+1, 0] - V_O2[j, 0])

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
    plt.plot(U[:, 0], U[:, i], label=param_name + " = " + str(param_values[i-1]))

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
for i in range(1, H2_speed[0].shape[0]):
    plt.plot(H2_speed[:, 0], H2_speed[:, i], label=param_name + " = " + str(param_values[i-1]))

plt.legend()
plt.title(r"$V_{H_2}$ speed")
plt.xlabel("Time (min)")
plt.ylabel("Speed (mL/min)")
plt.grid(alpha=0.5)
plt.savefig("Plots/H2_speed.png")
plt.show()

# Plot O2 speed vs Time
plt.figure()
for i in range(1, O2_speed[0].shape[0]):
    plt.plot(O2_speed[:, 0], O2_speed[:, i], label=param_name + " = " + str(param_values[i-1]))

plt.legend()
plt.title(r"$V_{O_2}$ speed")
plt.xlabel("Time (min)")
plt.ylabel("Speed (mL/min)")
plt.grid(alpha=0.5)
plt.savefig("Plots/O2_speed.png")
plt.show()


# Plot Faraday efficiency vs Time

if param_name == "U":
    theorical_speed = np.copy(U)
    theorical_speed[:, 1:] = (24.05e3*60)*theorical_speed[:, 1:]/(2*96485) # mol/s -> mL/min
    theorical_speed = theorical_speed[:-1, :]
    farad_eff = np.zeros(theorical_speed.shape)
    farad_eff[:, 0] = theorical_speed[:, 0]
    farad_eff[:, 1:] = H2_speed[:, 1:]/theorical_speed[:, 1:]

elif param_name == "I":
    theorical_speed = np.zeros(U.shape)
    theorical_speed[:, 1:] = (24.05e3*60)*np.tile(param_values, (U.shape[0], 1))/(2*96485) # mol/s -> mL/min
    theorical_speed[:, 0] = U[:, 0]
    theorical_speed = theorical_speed[:-1, :]
    farad_eff = np.zeros(theorical_speed.shape)
    farad_eff[:, 0] = theorical_speed[:, 0]
    farad_eff[:, 1:] = H2_speed[:, 1:]/theorical_speed[:, 1:]
else:
    theorical_speed = np.ones(U.shape)
    theorical_speed[:, 1:] = (24.05e3*60)*param_values/(2*96485)
    theorical_speed[:, 0] = U[:, 0]
    theorical_speed = theorical_speed[:-1, :]
    farad_eff = np.zeros(theorical_speed.shape)
    farad_eff[:, 0] = theorical_speed[:, 0]
    farad_eff[:, 1:] = H2_speed[:, 1:]/theorical_speed[:, 1:]

plt.figure()
for i in range(1, farad_eff[0].shape[0]):
    plt.plot(farad_eff[:, 0], farad_eff[:, i], label=param_name + " = " + str(param_values[i-1]))

plt.legend()
plt.title(r"Faraday efficiency")
plt.xlabel("Time (min)")
plt.ylabel("Faraday efficiency")
plt.grid(alpha=0.5)
plt.savefig("Plots/farad_eff.png")
plt.show()



# Plot energy efficiency vs Time
if param_name == "U" or param_name == "I":
    energy_consumption = np.copy(U)
    energy_consumption[0,1:] = np.zeros(U.shape[1]-1)
    for i in range(1, energy_consumption.shape[0]):
        energy_consumption[i, 1:] = energy_consumption[i-1, 1:] + param_values*U[i, 1:]*(U[i, 0] - U[i-1, 0])*60 # J
    
    energy_eff = np.zeros(energy_consumption.shape)
    energy_eff[:, 0] = energy_consumption[:, 0]
    energy_eff[:, 1:] = energy_consumption[:, 1:]/((285.8/24.05)*V_H2[:, 1:])

else:
    energy_consumption = np.ones(U.shape)
    energy_consumption[:, 0] = U[:, 0]
    energy_consumption[0,1:] = np.zeros(U.shape[1]-1)
    for i in range(1, energy_consumption.shape[0]):
        energy_consumption[i, 1:] = energy_consumption[i-1, 1:] + param_values*U[i, 1:]*(U[i, 0] - U[i-1, 0])*60
    
    energy_eff = np.zeros(energy_consumption.shape)
    energy_eff[:, 0] = energy_consumption[:, 0]
    energy_eff[:, 1:] = energy_consumption[:, 1:]/((285.8/24.05)*V_H2[:, 1:])


plt.figure()
for i in range(1, energy_eff[0].shape[0]):
    plt.plot(energy_eff[:, 0], energy_eff[:, i], label=param_name + " = " + str(param_values[i-1]))

plt.legend()
plt.title(r"Energy efficiency")
plt.xlabel("Time (min)")
plt.ylabel("Energy efficiency")
plt.grid(alpha=0.5)
plt.savefig("Plots/energy_eff.png")
plt.show()