import os
os.system("rm -rf anchor0 anchor1 anchor2 anchor3 anchor4 anchor5 anchor6 anchor7 anchor8 anchor9 anchor10")
os.system("python write_anchor.py --steps 10000")
os.system("python add_vectors_pdb.py")
os.system("python filetree.py --steps 1000")
os.system("python measure_com.py")
os.system("python run_md_anchors.py")



