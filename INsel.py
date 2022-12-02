#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys

print("This is the INCAR option available:")
print("1)Stu_relax")
print("2)vib")
print("3)NEB")
print("4)Fine_NEB")
print("5)STM")
print("6)DOS")
a = int(input("Please enter the number:"))

if a == 1:
    INCAR_name = "INCAR_Stru_relax"
elif a == 2:
    INCAR_name = "INCAR_vib"
elif a == 3:
    INCAR_name = "INCAR_NEB"
elif a == 4:
    INCAR_name = "INCAR_fine_NEB"
elif a == 5:
    INCAR_name = "INCAR_STM"
elif a == 6:
    INCAR_name = "INCAR_DOS"

cp_comm = 'cp /home/yczhang/work/incar/'+INCAR_name+' INCAR'
os.system(cp_comm)
print("已导入输入文件 ",INCAR_name)
