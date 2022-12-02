#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import subprocess

for root, dirs, files in os.walk(os.getcwd()):
    dir_list = dirs
    break

IS_dir_num = input("Folder number of initial state：")
FS_dir_num = input("Folder number of Final state：")
tar_dir_num = input("Folder number of target folder：")

for dir in dir_list:
    if dir.startswith(IS_dir_num):
        IS_dir = dir
        print("IS_dir is ",dir)
    if dir.startswith(FS_dir_num):
        FS_dir = dir
        print("FS_dir is ",dir)
    if dir.startswith(tar_dir_num):
        tar_dir = dir
        print("target_dir is ",dir)

cp1_comm = "cp " + IS_dir + "/CONTCAR " + tar_dir + "/CONTCAR1"
cp2_comm = "cp " + FS_dir + "/CONTCAR " + tar_dir + "/CONTCAR2"
cp3_comm = "cp " + IS_dir + "/POTCAR " + tar_dir + "/POTCAR"
cp4_comm = "cp " + IS_dir + "/KPOINTS " + tar_dir + "/KPOINTS"
cp5_comm = "cp /home/yczhang/work/incar/INCAR_NEB " + tar_dir + "/INCAR"
cp6_comm = "cp ../" + IS_dir + "/OUTCAR 00/OUTCAR"
cp7_comm = "cp ../" + FS_dir + "/OUTCAR 05/OUTCAR"

os.popen(cp1_comm)
os.popen(cp2_comm)
os.popen(cp3_comm)
os.popen(cp4_comm)
os.popen(cp5_comm)
os.chdir(tar_dir)
m = os.popen('nebmake.pl CONTCAR1 CONTCAR1 4')
print(m.readlines()[-1])
os.popen(cp6_comm)
os.popen(cp7_comm)
m = os.popen('nebavoid.pl 1')
for line in m.readlines():
    print(line)
time.sleep(5)
m = os.popen('nebmovie.pl  0')
print(m.readlines()[-2])
