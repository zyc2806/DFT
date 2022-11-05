import os
import shutil

#适合于单个原子替换，只适合于替换型原子掺杂
CARfile = []
num_select_start = 10 #被替换原子开始行数
num_select = 24  #被替换的原子数目
with open(r"1.vasp", 'r') as fp:
    CARfile = fp.readlines()
for i in range(num_select_start - 1, num_select_start + num_select - 1):
    select_atom = CARfile[i]
    CAR_filename = "POSCAR"
    CAR_name = str(i - num_select_start + 2) + "Cu_N3_Str"
    os.mkdir(CAR_name)
    CARfile_Path = CAR_name + "/" + CAR_filename
    f20 = CAR_name + "/" + "INCAR"
    f2 = 'INCAR'
    f30 = CAR_name + "/" + "KPOINTS"
    f3 = 'KPOINTS'
    f40 = CAR_name + "/" + "POTCAR"
    f4 = 'POTCAR'
    shutil.copyfile(f2, f20)
    shutil.copyfile(f3, f30)
    shutil.copyfile(f4, f40)
    with open(CARfile_Path, 'w') as fp:
        for number, line in enumerate(CARfile):
            if number not in [i]:
                fp.write(line)
    with open(CARfile_Path, 'a') as fp:
        fp.write("\n" + str(select_atom))
        fp.close()

