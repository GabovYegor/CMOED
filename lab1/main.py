import csv

with open('machine.data', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    vendorName = []
    ModelName = []
    MYCT = []
    MMIN = []
    MMAX = []
    CACH = []
    CHMIN = []
    CHMAX = []
    PRP = []
    ERP = []
    for row in spamreader:
        vendorName.append(row[0])
        ModelName.append(row[1])
        MYCT.append(int(row[2]))
        MMIN.append(row[3])
        MMAX.append(row[4])
        CACH.append(row[5])
        CHMIN.append(row[6])
        CHMAX.append(row[7])
        PRP.append(row[8])
        ERP.append(row[9])
    sortedMYCT = MYCT.sort()
    print(sorted(MYCT))

