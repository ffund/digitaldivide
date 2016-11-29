for i in range(1):
    everything = open("tmp/dlrate-"+str(i)+".txt", "r").read()
    all40 = everything[everything.rfind("[SUM]")+38:everything.rfind("[SUM]")+42]
    print all40
