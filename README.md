# DFT
Some scripts on DFT
- **xsd2car.pl** Fixing atoms in MS while generating POSCAR.
- **cluster.py** Calling the ASE package to generate a load-based cluster structure file.
- **vib_correct_ts.py** Elimination of the second imaginary frequency of the transition state according to OUTCAR.
- **droping.py** Generates multiple CAR files. Only applicable to the conversion of a loaded catalyst model to a substituted catalyst model. Before use, delete the coordinates of the originally loaded metal atoms in POSCAR or CONTCAR and subtract 1 from the number of atoms you wish to replace.
- **droping_.py** In addition to the functions of the previous script, this script can generate folders including INCAR, POTCAR, KPOINTS.The above files need to be present in the target folder.
