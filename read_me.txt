Running OpenMMVT Simulations
#########################################################################################################################################################################
What we need in the OpenMMVT simulation directory at the beginning:
1. topology file: system_TP4EW.parm7 
2. pdb file : system_TP4EW_mmvt_init.pdb ( originally system_nvt_output_last_frame.pdb file in the analysis section)
3. receptor index pickle file: receptor_cv_index ( originally receptor_cv_choice_index pickle file as named from the pickle_files directory in the analysis section)
4. ligand index pickle file:  ligand_cv_index ( originally ligand_cv_choice_index pickle file as named from the pickle_files directory in the analysis section)
5. box vectors pickle file: init_box_vectors (originally  nvt_simulation_box_vectors.pkl pickle file in the analysis section)
6. generate_init_structure.py – Present by default. 
#########################################################################################################################################################################
Run the scripts in the following order:
1. write_anchor.py  -  This script writes an anchor.py file that later on get placed in each of the anchor directory. These are the flags:
                '-na','--num_anchors', type = int, required = False, default = 9,"Number of anchors needed for milestoning"
                '-T','--temperature', type = float, required = False, default = 300.0,"Simulation Temperature"
                '-fa','--first_anchor', type = float, required = False, default = 1.0, "First anchor distance in Angstroms"
                '-ts','--timesteps', type = float, required = False, default = 0.002, "Timesteps"
                '-s','--steps', type = int, required = False, default = 100000, "Number of simulation steps"
#########################################################################################################################################################################
2. add_vectors_pdb.py  -  This script adds the box vector dimensions to the opdb file so that the OpenMM script reads its from there.
#########################################################################################################################################################################
3. filetree.py – This script does the following:
            a. Within each anchor, it creates the building folder  and places the generate_init_structure.py, system_TP4EW_mmvt_init.pdb and system_TP4EW.parm7 files in this directory.
            b. Within each anchor, it creates the md directory, and places the anchor.py file that is responsible for running MD simulations within each anchor. 
            c. These are the flags:
                '-na','--num_anchors', type = int, required = False, default = 9,"Number of anchors needed for milestoning"
                '-T','--temperature', type = float, required = False, default = 300.0,"Simulation Temperature"
                '-fa','--first_anchor', type = float, required = False, default = 1.0, "First anchor distance in Angstroms"
                '-ts','--timesteps', type = float, required = False, default = 0.002, "Timesteps"
                '-s','--steps', type = int, required = False, default = 100000, "Number of simulation steps"
#########################################################################################################################################################################
4. measure_com.py – This script iterates over each anchor and measures the center of mass within each anchor.
#########################################################################################################################################################################
5. run_md_anchors.py – This script runs MD simulations within each anchor
#########################################################################################################################################################################
