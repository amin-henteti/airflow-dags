import os
import shutil
import re
from pprint import pprint

for x in os.walk("."):
    root, dirs, files = x
    for file in files:
        if file.endswith('.srt'):
            # print(file)
            filename = os.path.join(root, file)
            with open(filename) as f:
                new_filename = os.path.join(root, file.replace('.srt', '.txt'))
                with open(new_filename, 'w') as g:
                    lines = f.read()
                    # print(re.findall(r'\n[\d:,>-].*?\n', lines)) #test pattern
                    clean = re.sub(r'[\d:,>-].*?\n', '\n', lines)
                    g.write(re.sub(r'\n{2,}', '\n', clean))
                    # print(clean)
                    # break
