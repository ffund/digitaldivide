for i in range(2):
    everything = open("tmp/dlrate-"+str(i)+".txt", "r").read()
    allline = everything[everything.rfind("[SUM]"):everything.rfind("receiver")]
    allnum = float(allline[allline.find("Bytes")+5: allline.rfind("bits")-2].strip())
    #print allnum
    ignore5 = everything[everything.find("[SUM]"):everything.find("- -")]
    ignorenum5 = float(ignore5[ignore5.find("Bytes")+5: ignore5.rfind("bits")-2].strip())
    #print ignorenum5
    not5 = everything[everything.find("10.00  sec"):]
    ignore10 = not5[not5.find("[SUM]"):not5.find("- -")]
    ignorenum10 = float(ignore10[ignore10.find("Bytes")+5: ignore10.rfind("bits")-2].strip())
    #print ignorenum10
    no10 = (allnum*12 - ignorenum5 - ignorenum10) / 10
    print no10

for i in range(2):
    everything = open("tmp/ulrate-"+str(i)+".txt", "r").read()
    allline = everything[everything.rfind("[SUM]"):everything.rfind("receiver")]
    allnum = float(allline[allline.find("Bytes")+5: allline.rfind("bits")-2].strip())
    #print allnum
    ignore5 = everything[everything.find("[SUM]"):everything.find("- -")]
    ignorenum5 = float(ignore5[ignore5.find("Bytes")+5: ignore5.rfind("bits")-2].strip())
    #print ignorenum5
    not5 = everything[everything.find("10.00  sec"):]
    ignore10 = not5[not5.find("[SUM]"):not5.find("- -")]
    ignorenum10 = float(ignore10[ignore10.find("Bytes")+5: ignore10.rfind("bits")-2].strip())
    #print ignorenum10
    no10 = (allnum*12 - ignorenum5 - ignorenum10) / 10
    print no10
for i in range(2):
    everything = open("tmp/ping-"+str(i)+".txt", "r").read()
    line = everything[everything.rfind("="):].split("/")
    ping = line[1]
    print ping
#PROBLEM: not sure if kbps or mbps. easy fix, but remember to do