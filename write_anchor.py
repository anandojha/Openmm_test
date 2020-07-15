import pickle as pk
import argparse

parser = argparse.ArgumentParser(description = "Arguments for OpenMMMVT")
parser.add_argument('-na','--num_anchors', type = int, required = False, default = 9, help = "Number of anchors needed for milestoning")
parser.add_argument('-T','--temperature', type = float, required = False, default = 300.0, help = "Simulation Temperature")
parser.add_argument('-fa','--first_anchor', type = float, required = False, default = 1.0, help = "First anchor distance in Angstroms")
parser.add_argument('-ts','--timesteps', type = float, required = False, default = 0.002, help = "Timesteps")
parser.add_argument('-s','--steps', type = int, required = False, default = 100000, help = "Number of simulation steps")
args = parser.parse_args()

num_anchors = args.num_anchors
temperature = args.temperature
steps = args.steps
timesteps = args.timesteps
first_anchor = args.first_anchor

rec_cv = "receptor_cv_index"
lig_cv = "ligand_cv_index"

with open(rec_cv, "rb") as f:
    rec_indices = pk.load(f)
with open(lig_cv, "rb") as f:
    lig_indices = pk.load(f)

anchors = [None] * (num_anchors + 2)
anchors[0] = first_anchor
anchors[1:3] = [anchors[0] + 0.5, anchors[0] + 1.0]
anchors[3:5] = [anchors[2] + 1.0, anchors[2] + 2.0]
anchors[5:7] = [anchors[4] + 1.5, anchors[4] + 3.0]
last_index = num_anchors + 1
for i in range (6+1,last_index+1):
    anchors[i] = anchors[i-1] + 2.0

filename = "anchor.py"
with open(filename, "w") as file:
    file.write ("from simtk.openmm.app import * "                                           + "\n") 
    file.write ("from simtk.openmm import *"                                                + "\n") 
    file.write ("from simtk.unit import *"                                                  + "\n") 
    file.write ("from sys import stdout"                                                    + "\n") 
    file.write ("import mmvtplugin"                                                         + "\n") 
    file.write ("from mmvtplugin import MmvtLangevinIntegrator, vectori, vectord"           + "\n") 
    file.write ("from time import time"                                                     + "\n") 
    file.write ("import numpy as np"                                                        + "\n") 
    file.write ("import os"                                                                 + "\n") 
    file.write ("from MmvtVoro import MmvtVoro as voro"                                     + "\n") 
    file.write ("from MmvtVoro import State2Pdb"                                            + "\n") 
    file.write ("prmtop = AmberPrmtopFile(PARM)"                                            + "\n") 
    file.write ("system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer, constraints=HBonds)"                                            + "\n") 
    file.write ("mypdb = PDBFile(INIT_PDB)"                                                   + "\n") 
    file.write ("lig_indices = " + str(lig_indices) + "\n") 
    file.write ("rec_indices = " + str(rec_indices) + "\n")    
    file.write ("integrator = MmvtLangevinIntegrator(" + str(temperature) + "*kelvin, 1/picosecond, " + str(timesteps) + "*picoseconds, DATA)" + "\n")     
    file.write ("anchors = " + str(anchors) + "\n") 
    file.write ("adjAnchors = [ADJ_ANCHORS]"                                                + "\n") 
    file.write ("steps = " + str(steps)                                                     + "\n") 
    file.write ("voro(INIT_PDB, ANCHOR_INDEX, lig_indices, rec_indices, anchors, integrator, system, adjAnchors, steps, ANCHOR)" + "\n") 
    file.write ("integrator.setCheckFreq(1)"                                               + "\n") 
    file.write ("platform = Platform.getPlatformByName('CUDA')"                             + "\n") 
    file.write ("properties = {'CudaDeviceIndex': '0', 'CudaPrecision': 'mixed'}"           + "\n") 
    file.write ("simulation = Simulation(prmtop.topology, system, integrator, platform, properties)"                                           + "\n") 
    file.write ("simulation.context.setPositions(mypdb.positions)"                          + "\n") 
    file.write ("simulation.context.setVelocitiesToTemperature(" + str(temperature) +"*kelvin)"                                                + "\n") 
    file.write ("simulation.reporters.append(PDBReporter(OUTPUT_PDB, 1000))"                + "\n") 
    file.write ("simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, potentialEnergy=True, temperature=True, volume=True))" + "\n") 
    file.write ("start_time = time()"                                                       + "\n") 
    file.write ("simulation.step(steps)"  + "\n") 
    file.write ("print(time() - start_time)"                                                + "\n") 
