# -*- coding: utf-8 -*-
import numpy as np
from ase.io import read, write
import os

#获取次最大虚频开始行
l_position = 0  #虚频振动方向部分在OUTCAR中的起始行数
with open('OUTCAR') as f_in:
    lines = f_in.readlines()
    wave_num = 0.0
    wave_tem = 0.0
    for num, line in enumerate(lines):
        if 'f/i' in line:
            exwave_tem = wave_tem
            wave_tem = float(line.rstrip().split()[6])
            if wave_tem > wave_num:  #获取次最大的虚频
                wave_num = exwave_tem
                l_position = num + 2
# ASE读POSCAR
model = read('POSCAR')
model_positions = model.get_positions()
num_atoms = len(model)
#print(model_positions)

# 获取虚频对应的OUTCAR部分
vib_lines = lines[l_position:l_position + num_atoms]  #振动部分
#print(vib_lines)
vib_dis = []
for line in vib_lines:
    #model_positions = [float(i) for i in line.rstrip().split()[:3]]
    vib_infor = [float(i)
                 for i in line.rstrip().split()[3:]]  # dx， dy， dz对应的那三列
    vib_dis.append(vib_infor)
vib_dis = np.array(vib_dis)  #将振动部分写到一个array中。

# 微调结构
new_positions = model_positions - vib_dis * 0.3
# 0.4是微调的校正因子，即虚频对应振动位移的0.4，具体多大自己根据经验调。
model.positions = new_positions

###保存结构
write('POSCAR_new-0.3', model,
      vasp5=True)  # POSCAR_new是微调后的结构，用于下一步的计算（别忘了把POSCAR_new改成POSCAR）。