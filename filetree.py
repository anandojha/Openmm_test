import os
from shutil import copyfile
from pathlib import Path
import fnmatch
import argparse

parser = argparse.ArgumentParser(description = "Arguments for OpenMMMVT")
parser.add_argument('-na','--num_anchors', type = int, required = False, default = 9, help = "Number of anchors needed for milestoning")
parser.add_argument('-T','--temperature', type = float, required = False, default = 300.0, help = "Simulation Temperature")
parser.add_argument('-fa','--first_anchor', type = float, required = False, default = 1.0, help = "First anchor distance in Angstroms")
parser.add_argument('-ts','--timesteps', type = float, required = False, default = 0.002, help = "Timesteps")
parser.add_argument('-s','--steps', type = int, required = False, default = 100000, help = "Number of simulation steps")
args = parser.parse_args()

num_anchors = args.num_anchors

sim_script = "anchor.py"
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "*.pdb"):
        holo_pdb = file
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, "*.parm7"):
        parm = file

pwd = os.getcwd()
system_name = pwd.split("/")[-1]
path = os.path.dirname(os.getcwd()) + "/" + system_name
anchors = ["anchor" + str(anchor) for anchor in range(num_anchors)]
for anchor_index, anchor in enumerate(anchors):
	os.mkdir(path + "/" + anchor)
	os.mkdir(path + "/" + anchor + "/building")
	os.mkdir(path + "/" + anchor + "/md")
	copyfile(path + "/" + holo_pdb, path + "/" + anchor + "/building/" + holo_pdb)
	copyfile(path + "/" + parm, path + "/" + anchor + "/building/" + parm)
	copyfile(path + "/" + parm, path + "/" + anchor + "/md/" + system_name + "_" + anchor + ".parm7")
	copyfile(path + "/" + sim_script, path + "/" + anchor + "/md/" + anchor + ".py")
	copyfile(path + "/generate_init_structure.py", path + "/" + "/" + anchor + "/building/generate_init_structure.py")
	generate_init_structure = Path(path + "/" + anchor + "/building/generate_init_structure.py")
	Anchor = generate_init_structure.read_text()
	Anchor = Anchor.replace("ANCHOR", str(anchor_index))
	generate_init_structure.write_text(Anchor)
	init_pdb = generate_init_structure.read_text()
	init_pdb = init_pdb.replace("INIT_PDB", "'" + path + "/" + anchor + "/md/" + system_name + "_" + anchor + "_init.pdb" + "'")
	generate_init_structure.write_text(init_pdb)
	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	parm_file = anchor_simulation_script.read_text()
	parm_file = parm_file.replace("PARM", "'" + system_name + '_' + anchor + ".parm7" + "'")
	anchor_simulation_script.write_text(parm_file)
	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	init_pdb = anchor_simulation_script.read_text()
	init_pdb = init_pdb.replace("INIT_PDB", "'" + path + "/" + anchor + "/md/" + system_name + "_" + anchor + "_init.pdb" + "'")
	anchor_simulation_script.write_text(init_pdb)
	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	data = anchor_simulation_script.read_text()
	data = data.replace("DATA", "'" + path + "/" + anchor + "/md/" + system_name + "_" + anchor + "_output.txt" + "'")
	anchor_simulation_script.write_text(data)
	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	anchor_num = anchor_simulation_script.read_text()
	anchor_num = anchor_num.replace("ANCHOR_INDEX", str(anchor_index))
	anchor_simulation_script.write_text(anchor_num)

	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	adj_anchor = anchor_simulation_script.read_text()
	adj_anchor = anchor_num.replace("ADJ_ANCHORS", str(anchor_index - 1) + ', ' + str(anchor_index + 1))
	anchor_simulation_script.write_text(adj_anchor)

	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	anchor_name = anchor_simulation_script.read_text()
	anchor_name = anchor_name.replace("ANCHOR", '"{}"'.format(anchor))
	anchor_simulation_script.write_text(anchor_name)
	anchor_simulation_script = Path(path + "/" + anchor + "/md/" + anchor + ".py")
	output_pdb = anchor_simulation_script.read_text()
	output_pdb = output_pdb.replace("OUTPUT_PDB", "'" + path + "/" + anchor + "/md/" + system_name + "_" + anchor + "_output.pdb" + "'")
	anchor_simulation_script.write_text(output_pdb)


temperature  = args.temperature
steps = args.steps
timesteps = args.timesteps
first_anchor = args.first_anchor
num_anchors = args.num_anchors 

for anchor_index, anchor in enumerate(anchors):
    command = 'python generate_init_structure.py --temperature {} --steps {} --timesteps {} --num_anchors {} --first_anchor {}'.format(temperature, steps, timesteps, num_anchors, first_anchor)
    os.chdir(path + "/" + anchor + "/building")
    os.system(command)
    command = ''
