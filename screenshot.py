#!/usr/bin/env python3

import os
import subprocess

folder = "/home/yuri/Dropbox/media/lego"
files = [os.path.join(folder, x) for x in os.listdir(folder)]

target = os.path.join(os.getcwd(), "test")
os.makedirs(target, exist_ok=True)

for file in files:
    name = f"{os.path.splitext(os.path.basename(file))[0]}.jpg"
    output = os.path.join(target, name)
    result = subprocess.run([
        "convert", 
        "-density", "300", 
        "-resize", "1000x1000", 
        "-strip", 
        "-quality", "70%", 
        "-alpha", "off",
        "-background", "white", 
        f"{file}[0]", f"{output}" 
    ], text=True, check=True)

# TODO
# [ ] Creare cartella di supporto nascosta
# [ ] Creare oggetto entry
# [ ] Salvare output intermedio
# [ ] Creare file HTML con link
# [ ] Evitare di fare thumbs in caso esista già
# [ ] form di ricerca https://www.lego.com/it-it/service/buildinginstructions/31009