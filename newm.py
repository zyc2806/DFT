#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os

os.popen("sed -i 's/EDIFF  = 1E-4/EDIFF = 1E-7/'  INCAR")
os.popen("sed -i 's/EDIFFG = -0.05/EDIFFG = -0.02/'  INCAR")
os.popen('mv CONTCAR POSCAR')
