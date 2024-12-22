#see I have to import file then run loops something like if string is not psk or **** type thingy then iterate and save right?
import os
import re
path= os.path.join("~/Music/iwd-manager","k.txt")
expanded_path = os.path.expanduser(path)
file = open(expanded_path, 'rt')

def reg():
    for i in file:
        if "*" in i:
            for x in i:
                regex= re.search(r"[^*]",x)
                
                if regex:
                    print(regex.group(),end="")