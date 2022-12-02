#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os

#获取虚频开始行
l_position = 0  #虚频振动方向部分在OUTCAR中的起始行数
with open('OUTCAR') as f_in:
    lines = f_in.readlines()
    wave_num = 0.0
    for num, line in enumerate(lines):
        if 'f/i' in line:
            wave_tem = float(line.rstrip().split()[6])
            if wave_tem > wave_num: #获取最大的虚频
                wave_num = wave_tem
                l_position = num+2
# 读POSCAR
with open('POSCAR') as f_pos:
    lines_pos = f_pos.readlines()

# 获取虚频对应的OUTCAR部分
num_atoms = sum([int(i) for i in lines_pos[6].rstrip().split()])
vib_lines = lines[l_position:l_position + num_atoms] #振动部分 7222到7248行

model_positions = []
vib_dis = []
for line in vib_lines:
    position = [float(i) for i in line.rstrip().split()[:3]]
    vib_infor = [float(i) for i in line.rstrip().split()[3:]] # dx， dy， dz对应的那三列
    model_positions.append(position)
    vib_dis.append(vib_infor)

# 微调结构
model_positions = np.array(model_positions)
vib_dis = np.array(vib_dis) #将振动部分写到一个array中。
new_positions = model_positions + vib_dis * 0.4 # 0.4是微调的校正因子，即虚频对应振动位移的0.4，具体多大自己根据经验调。

###保存结构
f_out = open('POSCAR_new','w')
f_out.writelines(lines_pos[:8])
f_out.write('Cartesian\n')
for i in new_positions:
    f_out.write(' '.join([str(coord) for coord in i]) + '  F  F  F\n')
f_out.close()
