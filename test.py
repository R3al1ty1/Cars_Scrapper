with open("Cars.txt") as f:
    lst = f.readlines()
lst = list(set(lst))
lst = sorted(lst)
#for i in range(len(lst)):
#    lst[i] = lst[i].replace('\n', '')
with open("Cars.txt", "w+") as f:
    for elem in lst:
        f.write(elem.replace(" ", "_").lower())
#for elem in lst:
#    print(elem)
