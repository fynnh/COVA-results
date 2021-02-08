import json
import os

with open("result.json") as tmp:
    data = json.load(tmp)

not_founds = set()
founds = set()
for target in data["possibleTargets"]:
    candidates = list()
    for constraint in data["constraints"]:
        if constraint["output"] == target["target"] and constraint["paths"]:
            candidates.append(constraint)
    if len(candidates) == 0:
        not_founds.add(target["target"])
        #print("not_found: " + target["javaClassName"]+":"+str(target["javaLineNumber"]))
    else:
        founds.add(target["target"])
        #print("found: " + target["javaClassName"]+":"+str(target["javaLineNumber"]))
real_founds = set()
errors = set()
for dirname in os.scandir():
    if not dirname.is_dir():
        continue
    test_f = os.path.join(dirname, "information.json")
    if not os.path.exists(test_f):
        continue
    with open(test_f) as tmp:
        info = json.load(tmp)
    if info["reachedDestination"]:
        real_founds.add(info["choosenOutput"])
    else:
        errors.add(info["choosenOutput"])
for rf in real_founds:
    if rf in errors:
        errors.delete(rf)
for error in errors:
    print(error)
print("result_not_founds: " + str(len(not_founds)))
print("result_true_positive: " + str(len(real_founds)))
print("result_false_positive: " + str(len(errors)))

