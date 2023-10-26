import mesa_reader as mr
import numpy as np
import matplotlib.pyplot as plt
# 15 solar mass
history = mr.MesaData('history.data')
profile = mr.MesaData('make_he_wd_me.data')
friendly_profile = mr.MesaData('Friendly_Profile.data')

element_names = ['h1', 'he3', 'he4', 'c12', 'n14', 'o16', 'o18', 'ne20', 'ne22', 'mg24']
num_element = len(element_names)
total_mass = 0.15
total_zone = len(profile.zone)
# h1_abundance norm
arr = np.empty((total_zone, num_element))
# fraction of mass interior to the outer boundary of this zone
log_xq = profile.logxq

xq = np.empty((total_zone, 1))

for i in range(len(profile.logxq)):
    xq[i] = 10**profile.logxq[i]

for i in range(total_zone):
    for j in range(num_element):
        new_element = getattr(profile, element_names[j])
        if i == 1023:
            arr[i, j] = new_element[i] * (profile.mass[i])
        else:
            arr[i, j] = new_element[i]*(profile.mass[i]-profile.mass[i+1])

xq = xq.T
arr = np.insert(arr, 0, xq, axis=1)
print(np.shape(arr))
np.savetxt('abundances.txt', arr, delimiter=' ')











