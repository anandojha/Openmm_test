import os

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


for j in range(0,anchor_count):
    os.chdir(current_path + "/" + "anchor" + str(j) + "/" + "md")
    command = "python anchor{}.py".format(j)
    os.system(command)
    os.chdir(current_path)
    command = ''
