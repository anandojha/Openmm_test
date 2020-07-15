import re
import pickle as pk
import os
import fnmatch

with open ("init_box_vectors", "rb") as f:
    box_vectors = pk.load(f)

box_vectors = str(box_vectors)
box_vectors = box_vectors.replace("Vec3", "")
box_vectors = re.findall('\d*\.?\d+',box_vectors)
for i in range(0, len(box_vectors)):
    box_vectors[i] = float(box_vectors[i])
box_vectors = tuple(box_vectors)
n = int(len(box_vectors)/3)
box_vectors = [box_vectors[i * n:(i + 1) * n] for i in range((len(box_vectors) + n - 1) // n )]

first_line = "CRYST1" + "   " + str(round(box_vectors[0][0] * 10, 3)) + "   " + str(round(box_vectors[1][1] * 10, 3)) + "   " + str(round(box_vectors[2][2] * 10, 3) ) + "  " + "90.00" + "  " + "90.00" + "  " + "90.00" + " " + "P 1" + "           " + "1"

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "*.pdb"):
        holo_pdb = file
        
with open(holo_pdb) as f:
    lines = f.readlines()
lines[0] = first_line + "\n"
with open(holo_pdb, "w") as f:
    f.writelines(lines)
