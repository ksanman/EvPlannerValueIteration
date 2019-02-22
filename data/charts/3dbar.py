import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

z=[[-97.0, -97.0, 3.0, 3.0],
 [ -98.0, -98.0, 2.0, 2.0],
 [ -99.0, -99.0, 1.0, 1.0],
 [-100.0, -100.0, 0.0, 0.0],
 [-100.0, -100.0, 0.0, 0.0]]

x = np.array([0,1,2,3,4])
y = np.array([0,1,2,3])
#z = np.arange(-10, 10, 1)
z = np.array(z)

#x, y = np.meshgrid(x, y, copy=False)

fig=plt.figure()

xlabels = x
xpos = np.arange(x.shape[0])
ylabels = y
ypos = np.arange(y.shape[0])
rewardScale = np.arange(z.min(), z.max(), 1).size + 1
zlabels = np.arange(z.min(), z.max(), rewardScale/(len(z)/2))
zpos = z.ravel()

xposM, yposM = np.meshgrid(xpos, ypos, copy=False)

dx=0.5
dy=0.5
zpos = 2* ((zpos - min(zpos))/np.float(max(zpos) - min(zpos))) - 1
dz = zpos
zpos = np.zeros_like(zpos)

ax=fig.gca(projection='3d')

ax.w_xaxis.set_ticks(xpos + dx/2.)
ax.w_xaxis.set_ticklabels(xlabels)
ax.w_yaxis.set_ticks(ypos + dy/2.)
ax.w_yaxis.set_ticklabels(ylabels)
#ax.w_zaxis.set_ticks(np.arange(len(dz)/2))
#ax.w_zaxis.set_ticklabels(zlabels)
ax.set_xlabel('Time')
ax.set_ylabel('Battery')
ax.set_zlabel('Reward')

ax.view_init(elev=47, azim=-155)
#ax.dist = 15

cmap = cm.get_cmap('coolwarm') # Get desired colormap - you can change this!
max_height = np.max(dz)   # get range of colorbars so we can normalize
min_height = np.min(dz)
# scale each z to [0,1], and get their rgb values
rgba = [cmap((k-min_height)/max_height) for k in dz] 

ax.bar3d(xposM.ravel(), yposM.ravel(), zpos, dx, dy, dz, color = rgba)
ax.autoscale(tight=True) 
plt.tight_layout()
plt.show()