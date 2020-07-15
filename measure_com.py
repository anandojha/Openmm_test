import os
import numpy as np
import mdtraj as md
import fnmatch
import pickle as pk

current_path = os.getcwd()
anchor_count = 0
for root, dirs, files in os.walk(current_path):
    for name in dirs:
        if name.startswith("anchor"):
            anchor_count = anchor_count + 1
current_path = os.getcwd()
anchor_count = 0
for root, dirs, files in os.walk(current_path):
    for name in dirs:
        if name.startswith("anchor"):
            anchor_count = anchor_count + 1

rec_cv = "receptor_cv_index"
with open (rec_cv, "rb") as f:
    rec = pk.load(f) 
lig_cv = "ligand_cv_index"
with open (lig_cv, "rb") as f:
    lig = pk.load(f) 
    
def init_delta_com(pdb, lig, rec):
        traj = md.load(pdb)
        positions = traj.xyz[0]
        topology = traj.topology
        lig_weighted_coordinates = map(lambda atom, mass, total_mass: (atom*mass)/total_mass, [positions[atom] for atom in lig], [topology.atom(atom).element.mass for atom in lig], [sum(topology.atom(atom    ).element.mass for atom in lig) for i in range(len(lig))])
        rec_weighted_coordinates = map(lambda atom, mass, total_mass: (atom*mass)/total_mass, [positions[atom] for atom in rec], [topology.atom(atom).element.mass for atom in rec], [sum(topology.atom(atom    ).element.mass for atom in rec) for i in range(len(rec))])
        lig_com = [sum(lig_coord) for lig_coord in zip(*lig_weighted_coordinates)]
        rec_com = [sum(rec_coord) for rec_coord in zip(*rec_weighted_coordinates)]
        init_delta_com = 10 * np.sqrt(sum(map(lambda lig, rec: (lig-rec)**2, lig_com, rec_com))) #multiply by ten to convert from nanometers to angstroms 
        return init_delta_com
    
anchor_com_list = []
for j in range(0,anchor_count):
    os.chdir(current_path + "/" + "anchor" + str(j) + "/" + "md")
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, "*_init.pdb"):
            pdb = file
    com = init_delta_com(pdb, lig, rec)
    anchor_com_list.append(com)
os.chdir(current_path)
com_list = []
for i in anchor_com_list:
    com_list.append(round(i, 2))
print(com_list)