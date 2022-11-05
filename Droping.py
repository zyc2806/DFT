#适合于单个原子替换，只适合于替换型原子掺杂
CARfile = []
num_select_start = 10 #被替换原子开始行数
num_select = 24  #被替换的原子数目
with open(r"1.vasp", 'r') as fp:
    CARfile = fp.readlines()
for i in range(num_select_start - 1, num_select_start + num_select - 1):
    select_atom = CARfile[i]
    CAR_name = "POSCAR" + str(i - num_select_start + 2)
    with open(CAR_name, 'w') as fp:
        for number, line in enumerate(CARfile):
            if number not in [i]:
                fp.write(line)
    with open(CAR_name, 'a') as fp:
        fp.write("\n" + str(select_atom))
        fp.close()
