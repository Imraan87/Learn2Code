P = py.sys.path;

a = py.str('C:\Users\Imraan\Desktop\Learn2Code\Python\VirtEnv27_64\Lib\site-packages');

insert(P,int32(0),'modpath')
insert(P,int32(10),a)

py.sys.path


matplotlib = py.importlib.import_module('matplotlib')
pyvisa     = py.importlib.import_module('pyvisa')
scipy      = py.importlib.import_module('scipy')




import matplotlib.pylab as pl 
import smithplot
from smithplot import SmithAxes

fig = pl.figure() 
ax1 = fig.add_subplot(121) 
ax1.plot([(1, 2), (3, 4)], [(4, 3), (2, 3)]) 
ax2 = fig.add_subplot(122, projection='smith') 
pl.show()