from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from MmvtVoro import InitPdb as init_pdb
from MmvtVoro import AmberParmBox
from sys import stdout
from time import time
import os
import fnmatch
import numpy as np
import pickle as pk
import argparse

parser = argparse.ArgumentParser(description = "Arguments for OpenMMMVT")
parser.add_argument('-T','--temperature', type = float, required = True, help = " Simulation Temperature")
parser.add_argument('-na','--num_anchors', type = int, required = True,  help = "Number of anchors needed for milestoning")
parser.add_argument('-fa','--first_anchor', type = float, required = True,  help = "first anchor distance in Angstroms")
parser.add_argument('-ts','--timesteps', type = float, required = True,  help = "Timesteps")
parser.add_argument('-s','--steps', type = int, required = True, help = "Number of simulation steps")
args = parser.parse_args()


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "*.pdb"):
        holo_pdb = file
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "*.parm7"):
        parm = file

rec_cv = "../../"  + "receptor_cv_index"
lig_cv = "../../"  + "ligand_cv_index"

with open(rec_cv, "rb") as f:
    rec_indices = pk.load(f)
with open(lig_cv, "rb") as f:
    lig_indices = pk.load(f)

num_anchors = args.num_anchors
temperature = args.temperature
steps = args.steps
timesteps = args.timesteps
first_anchor = args.first_anchor

anchors = [None] * (num_anchors + 2)
anchors[0] = first_anchor
anchors[1:3] = [anchors[0] + 0.5, anchors[0] + 1.0]
anchors[3:5] = [anchors[2] + 1.0, anchors[2] + 2.0]
anchors[5:7] = [anchors[4] + 1.5, anchors[4] + 3.0]
last_index = num_anchors + 1
for i in range (6+1,last_index+1):
    anchors[i] = anchors[i-1] + 2.0

prmtop = AmberPrmtopFile(parm)
system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer, constraints=HBonds)
mypdb = PDBFile(holo_pdb)
integrator = LangevinIntegrator(float(temperature)*kelvin, 1/picosecond, float(timesteps)*picoseconds)
init_pdb(holo_pdb, ANCHOR, lig_indices, rec_indices, anchors, system)
platform = Platform.getPlatformByName('CUDA')
properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}
simulation = Simulation(prmtop.topology, system, integrator, platform, properties)
simulation.context.setPositions(mypdb.positions)
simulation.minimizeEnergy()
simulation.context.setVelocitiesToTemperature(float(temperature)*kelvin)
simulation.reporters.append(PDBReporter(INIT_PDB, steps))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True,
        potentialEnergy=True, temperature=True, volume=True))
simulation.step(steps)
