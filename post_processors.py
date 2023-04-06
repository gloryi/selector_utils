import sys
import os
from filesutils import OUTDIR, csv_to_list


commands = [] 
commands.append("fileslnsorted")

if len(sys.argv) >=2:
    processor = sys.argv[1]
    files = sys.argv[2:]
else:
    print("INDEX")
    print(commands)
    exit()

print(files)
if processor == commands[0]:
    for outfile in files:

        data = csv_to_list(os.path.join(OUTDIR, outfile+".csv"))
        index = os.path.join(OUTDIR, os.path.basename(outfile))

        isExist = os.path.exists(index)

        if not isExist:
            os.makedirs(index)

        for line in data:
            order_n, path_orig = line
            os.symlink(path_orig, os.path.join(index, order_n))

else:
    print(commands)

