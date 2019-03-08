import  csv

def gettotal(path):
    reader=csv.reader(open(path,"r"))
    num=0
    alldata=0
    for item in reader:
        if num==0:
            pass
        else:
            adddata=eval(item[13])
            alldata+=adddata
        num+=1

    return alldata/num


path=r"C:\Users\xuhao_yang\PycharmProjects\day21\csv\000001.csv"
print(gettotal(path))