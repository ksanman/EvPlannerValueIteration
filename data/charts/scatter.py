from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

z=[[-97.0, -97.0, 3.0, 3.0],
 [ -98.0, -98.0, 2.0, 2.0],
 [ -99.0, -99.0, 1.0, 1.0],
 [-100.0, -100.0, 0.0, 0.0],
 [-100.0, -100.0, 0.0, 0.0]]

x = np.array([0,1,2,3,4])
y = np.array([0,1,2,3])
#z = np.arange(-10, 10, 1)
z = np.array(z)
z = z.flatten()
#z = 2* ((z - min(z))/np.float(max(z) - min(z))) - 1
x, y = np.meshgrid(x, y, copy=False)

fig = plt.figure()
ax = fig.gca(projection='3d')

x = x
y = y
z = z

#ax.plot(x, y, zs= 0)

ax.scatter(x, y, z, c = z<0, s = 20, cmap = 'coolwarm')

ax.set_xlabel('Time')
ax.set_ylabel('Battery')
ax.set_zlabel('Reward')
ax.view_init(elev=47, azim=-155)
plt.tight_layout()
plt.show()