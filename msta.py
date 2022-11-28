#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import pandas as pd
import numpy as np


def is_not_empty(a):
    return len(a) != 0


def out_str(a):
    m = os.popen(a)
    return str(m.readlines())


for root, dirs, files in os.walk(os.getcwd()):
    dir_list = dirs
    break
dir_list.remove('.ipynb_checkpoints')

if os.path.lexists('INCAR'):
    print('----------------------------')
    cdir_str = os.getcwd()
    path_list = cdir_str.split("/")
    cur_filename = path_list[-1]
    print(cur_filename)
    INCAR_path = 'INCAR'
    OUTCAR_path = 'OUTCAR'
    vib_path = dir_list[0]
    vib_line_path = vib_path + '/' + 'line.dat'
    vib_data_path = vib_path + '/' + 'vib.dat'
    INCAR_IBRION = 'grep IB ' + INCAR_path
    INCAR_EDIFFG = 'grep EDIFFG ' + INCAR_path
    INCAR_EDIFF = 'grep EDIFF ' + INCAR_path
    INCAR_IMAGES = 'grep IMAGES ' + INCAR_path
    INCAR_NFEE = 'grep NFREE ' + INCAR_path
    OUTCAR_reach = 'grep reach ' + OUTCAR_path
    IB = out_str(INCAR_IBRION)
    EG = out_str(INCAR_EDIFFG)
    ED = out_str(INCAR_EDIFF)
    IM = out_str(INCAR_IMAGES)
    NF = out_str(INCAR_NFEE)
    SL = out_str(OUTCAR_reach)
    if 'IBRION = 1' in IB:
        if is_not_empty(IM):
            print('过渡态插点')
        else:
            print('过渡态精修')
            if ('EDIFF  = 1E-7' in ED) and ('EDIFFG = -0.02' in EG) and (is_not_empty(SL)):
                print('已达最大精度收敛')
            elif (('EDIFF  = 1E-7' not in ED) or ('EDIFFG = -0.02' not in EG)) and (is_not_empty(SL)):
                print('当前任务已收敛，可提高收敛精度')
    elif 'IBRION = 2' in IB:
        print('稳态')
        if ('EDIFF  = 1E-7' in ED) and ('EDIFFG = -0.02' in EG) and (is_not_empty(SL)):
            print('已达最大精度收敛')
        elif (('EDIFF  = 1E-7' not in ED) or ('EDIFFG = -0.02' not in EG)) and (is_not_empty(SL)):
            print('当前任务已收敛，可提高收敛精度')
    if os.path.lexists(vib_path):
        print('频率任务已建立')
        os.systems('grep F= OSZICAR > line.dat')
        line_dat = pd.read_csv(vib_line_path, header=None, sep='\s+')
        n = line_dat.shape[0] % 6
        if n == 1:
            print('频率计算已结束，请注意检查频率')
            os.systems('grep cm-1 OUTCAR > vib.dat')
            vib_dat = pd.read_csv(vib_data_path, header=None,
                                  names=['id', 'f', '=', 'Hz', 'THz', '2Pinum', '2piHz', 'cm_num', 'cm', 'meV_num',
                                         'meV'], sep='\s+')
            m = vib_dat[vib_dat['f'] == 'f/i=']['2piHz']
            print("虚频个数为:", m.count())
            m_array = np.array(m)
            i_50_num = 0
            for k in m_array:
                if float(k) > 50:
                    i_50_num = i_50_num + 1
            print("大于50cm-1的个数为", i_50_num, '，为:')
            for k in m_array:
                if float(k) > 50:
                    print('  ', k, '  cm-1')
            os.remove('line.dat')
        os.remove('line.dat')
else:
    for dirs in dir_list:
        print('----------------------------')
        print(dirs)
        INCAR_path = dirs + '/INCAR'
        OUTCAR_path = dirs + '/OUTCAR'
        vib_path = dirs + '/' + dirs + "fc"
        vib_line_path = vib_path + '/' + 'line.dat'
        vib_data_path = vib_path + '/' + 'vib.dat'
        INCAR_IBRION = 'grep IB ' + INCAR_path
        INCAR_EDIFFG = 'grep EDIFFG ' + INCAR_path
        INCAR_EDIFF = 'grep EDIFF ' + INCAR_path
        INCAR_IMAGES = 'grep IMAGES ' + INCAR_path
        INCAR_NFEE = 'grep NFREE ' + INCAR_path
        OUTCAR_reach = 'grep reach ' + OUTCAR_path
        IB = out_str(INCAR_IBRION)
        EG = out_str(INCAR_EDIFFG)
        ED = out_str(INCAR_EDIFF)
        IM = out_str(INCAR_IMAGES)
        NF = out_str(INCAR_NFEE)
        SL = out_str(OUTCAR_reach)
        if 'IBRION = 1' in IB:
            if is_not_empty(IM):
                print('过渡态插点')
            else:
                print('过渡态精修')
                if ('EDIFF  = 1E-7' in ED) and ('EDIFFG = -0.02' in EG) and (is_not_empty(SL)):
                    print('已达最大精度收敛')
                elif (('EDIFF  = 1E-7' not in ED) or ('EDIFFG = -0.02' not in EG)) and (is_not_empty(SL)):
                    print('当前任务已收敛，可提高收敛精度')
        elif 'IBRION = 2' in IB:
            print('稳态')
            if ('EDIFF  = 1E-7' in ED) and ('EDIFFG = -0.02' in EG) and (is_not_empty(SL)):
                print('已达最大精度收敛')
            elif (('EDIFF  = 1E-7' not in ED) or ('EDIFFG = -0.02' not in EG)) and (is_not_empty(SL)):
                print('当前任务已收敛，可提高收敛精度')
        if os.path.lexists(vib_path):
            print('频率任务已建立')
            os.systems('grep F= OSZICAR > line.dat')
            line_dat = pd.read_csv(vib_line_path, header=None, sep='\s+')
            n = line_dat.shape[0] % 6
            if n == 1:
                print('频率计算已结束，请注意检查频率')
                os.systems('grep cm-1 OUTCAR > vib.dat')
                vib_dat = pd.read_csv(vib_data_path, header=None,
                                      names=['id', 'f', '=', 'Hz', 'THz', '2Pinum', '2piHz', 'cm_num', 'cm', 'meV_num',
                                             'meV'], sep='\s+')
                m = vib_dat[vib_dat['f'] == 'f/i=']['2piHz']
                print("虚频个数为:", m.count())
                m_array = np.array(m)
                i_50_num = 0
                for k in m_array:
                    if float(k) > 50:
                        i_50_num = i_50_num + 1
                print("大于50cm-1的个数为", i_50_num, '，为:')
                for k in m_array:
                    if float(k) > 50:
                        print('  ', k, '  cm-1')
                os.remove('line.dat')
            os.remove('line.dat')