import mesa_reader as mr
import numpy as np
import matplotlib.pyplot as plt

# 15 solar mass
history = mr.MesaData('history.data')
profile = mr.MesaData('make_he_wd_me.data')
friendly_profile = mr.MesaData('Friendly_Profile.data')
element_names = ['h1', 'he3', 'he4', 'c12', 'n14', 'o16', 'o18', 'ne20', 'ne22', 'mg24']
num_element = len(element_names)

# compute net mass of elements
total_masses = []
for element in element_names:
    new_element = getattr(profile, element)
    element_mass = 0
    for i in range(len(profile.zone)):
        element_mass = element_mass + new_element[i] * profile.mass[i]
    total_masses.append(element_mass)

element_averages = []
for i in range(len(element_names)):
    element_averages.append(total_masses[i] / sum(total_masses))

print(element_averages)

# assume 0.8 solar merged object, 0.55 inside is 50/50 Carbon oxygen, outside 0.25 has the above distribution

friendly_zones = len(friendly_profile.zone)
arr = np.empty((friendly_zones, num_element + 1))
for i in range(friendly_zones):
    arr[i, 0] = friendly_profile.mass[i]

# fill with average abundances
for i in range(len(element_names)):

    for j in range(friendly_zones):
        arr[j, i + 1] = element_averages[i]

# inserting CO core < 0.55
CO_Core_Abundance = [0, 0, 0, 0.5, 0, 0.5, 0, 0, 0, 0]
for i in range(len(element_names)):

    for j in range(friendly_zones):

        if arr[j, 0] > 0.25:
            arr[j, i + 1] = CO_Core_Abundance[i]

# swap mass coordinate to xq ???
start = 0
for i in range(friendly_zones):
    arr[i, 0] = start + 10**(friendly_profile.logxq[i])

top_line = [friendly_zones, num_element]
print(arr, np.shape(arr))
np.savetxt('abundances.txt', arr, delimiter=' ')

with open('abundances.txt', 'r') as f:
    lines = f.readlines()

# create a new row to insert
new_row = str(top_line[0]) + ' ' + str(top_line[1]) + '\n'

# insert the new row at the top of the file
lines.insert(0, new_row)

# open the output file for writing
with open('abund.dat', 'w') as f:
    f.writelines(lines)
