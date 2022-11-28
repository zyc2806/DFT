#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import pandas as pd

os.systems('qstat -a > stat.dat')
dat = pd.read_csv("stat.dat", header=None, skiprows=5,
                  names=['id', 'user', 'que', 'name', 'idx', 'nodes', 'tasks', '--', 'a', 'stat', 'time'], sep='\s+')
que_dic = {'platinum': 0, 'gold': 0, 'copper': 0, 'silver': 0}
que_dic['platinum'] = sum(dat[(dat['que'] == 'platinum') & (dat['stat'] == 'Q')]['nodes'])
que_dic['gold'] = sum(dat[(dat['que'] == 'gold') & (dat['stat'] == 'Q')]['nodes'])
que_dic['copper'] = sum(dat[(dat['que'] == 'copper') & (dat['stat'] == 'Q')]['nodes'])
que_dic['silver'] = sum(dat[(dat['que'] == 'silver') & (dat['stat'] == 'Q')]['nodes'])
print(que_dic)
key_zero_element = 0
que_name = ''
wating_num = 1000
for i in que_dic:
    if que_dic[i] == 0:
        que_name = i
        key_zero_element = 1
        break
if key_zero_element == 0:
    for i in que_dic:
        if que_dic[i] < wating_num:
            wating_num = que_dic[i]
            que_name = i
os.remove('stat.dat')
os.systems('qstat -q ' + i)
