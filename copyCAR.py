#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys


I_fold = sys.argv[1]
F_fold = sys.argv[2]

if I_fold != '0':
    print("Initial folder：",I_fold)
else:
    I_fold = os.getcwd()
    print("Initial folder：",I_fold)
if F_fold != '0':
    print("Final folder：",F_fold)
else:
    F_fold = os.getcwd()
    print("Final folder：",F_fold)

cp1_comm = "cp " + I_fold + "/POTCAR " + F_fold + "/POTCAR"
cp2_comm = "cp " + I_fold + "/KPOINTS " + F_fold + "/KPOINTS"
cp3_comm = "cp " + I_fold + "/CONTCAR " + F_fold + "/POSCAR"

os.popen(cp1_comm)
os.popen(cp2_comm)
os.popen(cp3_comm)
print("CONTCAR, KPOINTS, POTCAR from the initial folder have been transferred to the final folder")
