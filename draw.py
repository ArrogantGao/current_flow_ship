import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from global_land_mask import globe

fig=plt.figure()#设置一个画板，将其返还给fig
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, edgecolor='black')
# coastlines方法使用resolution关键字
ax.coastlines(resolution='50m')
# add_feature方法中,则要调用cfeature对象的with_scale方法
ax.add_feature(cfeature.OCEAN.with_scale('50m'))
path = np.loadtxt('path.txt')
x = path[:, 0]
y = path[:, 1]
plt.scatter(x, y, color = 'red', s = 2)


a = []
b = []
c = []
d = []
v = np.loadtxt('v.txt')
for v_i in v:
    lon, lat, v_x, v_y = v_i
    if lon%5 == 0 and lat%5 == 0 and globe.is_land(lat, lon) == 0:
        a.append(lon)
        b.append(lat)
        c.append(v_x)
        d.append(v_y)
plt.quiver(a, b, c, d)

plt.savefig("path_in_flow.jpg")

plt.close()