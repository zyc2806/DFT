#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time

cdir_str = os.getcwd()
path_list = cdir_str.split("/")
cur_filename = path_list[-1]
vib_dir = cur_filename+"fc"
vaspkit_402_comm = '(echo 402; echo 2; echo 2;echo 0 0.425;echo 1;echo 1-3)|vaspkit > vaspkit.out'
mkdir_comm = 'mkdir '+ vib_dir
cp1_comm = 'cp POTCAR '+vib_dir+'/POTCAR'
cp2_comm = 'cp KPOINTS '+vib_dir+'/KPOINTS'
cp3_comm = 'cp /home/yczhang/work/incar/INCAR_vib '+vib_dir+'/INCAR'
cp4_comm = 'cp CONTCAR_FIX '+vib_dir+'/POSCAR'
os.system(vaspkit_402_comm)
os.system(mkdir_comm)
time.sleep(1)
os.system(cp1_comm)
os.system(cp2_comm)
os.system(cp3_comm)
os.system(cp4_comm)
print("已建立文件夹及输入文件 ",vib_dir)
