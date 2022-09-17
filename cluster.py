import ase
from ase.cluster.cubic import FaceCenteredCubic
surfaces=[(1,0,0),(1,1,1),(1,-1,1)] 
layers= [6,5, -1]
atoms= FaceCenteredCubic('Cu',surfaces, layers)
from ase.io import read, write
write('slab.xyz',atoms, format='xyz')