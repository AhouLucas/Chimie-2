from sys import argv

if argv[1] == "help":
    print(
"""
ph create [type] [pH] [volume] [source mol/L]
ph modify [type] [pH before] [volume before] [pH after] [source mol/L]

[type]: acid | base
""")

elif argv[1] == "create":
    if len(argv) != 6:
        print("Invalid number of arguments")
        exit(1)

    type = argv[2]
    ph = float(argv[3])
    volume = float(argv[4])
    sourceSol = float(argv[5])

    if type != "acid" and type != "base":
        print("Invalid type")
        exit(1)
    if (type == "acid" and ph > 7) or (type == "base" and ph < 7):
        print("Invalid pH")
        exit(1)

    if ph < 7:
        volSol = 10**(-ph) * volume / sourceSol
    else:
        volSol = 10**(ph-14) * volume / sourceSol

    print(f"Volumes for {volume}L of solution with pH {ph} from {type} solution with concentration {sourceSol} mol/L:")
    print(f"Water: {volume - volSol}L")
    print(f"Solution: {volSol}L")

elif argv[1] == "modify":
    if len(argv) != 7:
        print("Invalid number of arguments")
        exit(1)

    type = argv[2]
    phBefore = float(argv[3])
    volumeBefore = float(argv[4])
    phAfter = float(argv[5])
    sourceSol = float(argv[6])

    if type != "acid" and type != "base":
        print("Invalid type")
        exit(1)
    if (type == "acid" and 7 < phBefore < phAfter) or (type == "base" and phAfter < phBefore < 7):
        print("Invalid pH")
        exit(1)

    if type == "acid":
        molBefore = 10**(-phBefore) * volumeBefore
        if phAfter > phBefore:
            waterAdd = (volumeBefore * 10**(-phAfter) - molBefore) / (-10**(-phAfter))
            solAdd = 0
        else:
            solAdd = (volumeBefore * 10**(-phAfter) - molBefore) / (sourceSol - 10**(-phAfter))
            waterAdd = 0
    else:
        molBefore = 10**(phBefore-14) * volumeBefore
        if phAfter < phBefore:
            waterAdd = (volumeBefore * 10**(phAfter-14) - molBefore) / (-10**(phAfter-14))
            solAdd = 0
        else:
            solAdd = (volumeBefore * 10**(phAfter-14) - molBefore) / (sourceSol - 10**(phAfter-14))
            waterAdd = 0

    print(f"Added volumes to go from {volumeBefore}L of solution with pH {phBefore} to a solution with pH {phAfter} from {type} solution with concentration {sourceSol} mol/L:")
    print(f"Water: {waterAdd}L")
    print(f"Solution: {solAdd}L")

else: 
    print("Invalid command")
    exit(1)