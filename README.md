# DFT
Some scripts on DFT
- **xsd2car.pl** Fixing atoms in MS while generating POSCAR.(This script was collected from the internet as a backup)
- **cluster.py** Calling the ASE package to generate a load-based cluster structure file.
- **vib_correct_ts.py** Elimination of the second imaginary frequency of the transition state according to OUTCAR.
- **droping.py** Generates multiple CAR files. Only applicable to the conversion of a loaded catalyst model to a substituted catalyst model. Before use, delete the coordinates of the originally loaded metal atoms in POSCAR or CONTCAR and subtract 1 from the number of atoms you wish to replace.
- **droping_1.py** In addition to the functions of the previous script, this script can generate folders including INCAR, POTCAR, KPOINTS.The above files need to be present in the target folder.
- **pymatgen_usage_Chinese.md** A simple manual for using pymatgen in Chinese.
- **mol_tran.ipynb** This script transfers molecule A from the surface of model A to the new substrate model B. It can be used for the replication of reaction paths on different surfaces. Please prepare the reaction pathway individual steps CONTCAR in different subfolders before use. These subfolders, named 'BASE' for the substrate B model and the ipynb file should be placed in the same directory. Please note that this is only suitable for cases where the A and B cell parameters are the same.
- **que.py** Automatic job submission to the queue with the lowest number of currently waiting tasks for the XMU Fu_Lab Xiangan server.
- **msta.py** This is a script that fits my own file naming conventions and input parameters to detect the calculation process of a task and to view the virtual frequency of a structure more easily.
