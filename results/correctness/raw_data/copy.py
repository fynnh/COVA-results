import os
from random import randrange
import json
from natsort import natsorted, ns
for f in os.scandir():
    if not ".json" in f.name:
        continue
    print(f)
    with open(f) as tmp:
        data = json.load(tmp)
    numbers = set()
    targets = data["possibleTargets"]
    if False:
        for target in data["possibleTargets"]:
            if not int(target["javaLineNumber"]) == -1:
                print(target["javaLineNumber"])
                targets.append(target)
    print("Targets: {}".format(len(targets)))
    if len(targets) < 20:
        for i in range(0, len(targets)):
            numbers.add(i)
    else:
        while len(numbers) < 20:
            numbers.add(randrange(len(targets)))
    csv_lines = list()
    tex_lines = list()
    for number in numbers:
        target = targets[number]
        target_str = target["target"]
        constraint = None
        for cst in data["constraints"]:
            if cst["output"] == target_str:
                constraint = cst
        #print(target)
        #print(constraint)
        filename = target["target"].replace("COVA_CONSTRAINT_INFORMATION:","") 
        #+ " - " + target["javaClassName"]+":"+str(target["javaLineNumber"])
        csv= filename + ";"
        tex = "\\Verb|" + filename + "| & "
        print(filename)
        if constraint:
            if len(constraint["paths"]) == 0:
                print("No path to target")
                csv += "No path to target activity; ;"
                tex += "No path to target activity & & "
            else:
                for path in constraint["paths"][0]:
                    csv += path["activity"] + str(path["values"]) + ","
                    tex += "\\Verb|" + path["activity"] + str(path["values"]) + "|, "
                    print(path["activity"])
                    print(path["values"])
                csv = csv[:-1]
                tex = tex[:-2]
                csv += "; ;"
                tex += " & & "
                print()
        else:
            csv += "No Constraint; ;"
            tex += "No Constraint & & "
        csv += "\n"
        csv_lines.append(csv)
        tex += "\\\\\n"
        tex_lines.append(tex)
    csv = "Target; Path; Correct; Reason\n"
    tex = "\\begin{table}[!ht]\n"
    tex += "\\begin{tabular}{lHll}\n"
    tex += "Target & Path & Correct & Reason\\\\\n"
    for c in natsorted(csv_lines):
        csv += c
    for t in natsorted(tex_lines):
        tex += t
    tex += "\end{tabular}\n"
    tex += "\end{table}"
    with open(f.name[:f.name.rindex(".")]+".csv", "w") as tmp:
        tmp.write(csv)
    with open(f.name[:f.name.rindex(".")]+".tex", "w") as tmp:
        tmp.write(tex)
    print(csv)
        
    
    
