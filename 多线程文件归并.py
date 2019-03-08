import csv
import threading

def thread1(file,e1,e2):
    path=r"C:\Users\xuhao_yang\PycharmProjects\day21\csv\000001.csv"
    reader=csv.reader(open(path,"r"))
    alllist=[]
    for item in reader:
        alllist.append(item)
    for line in alllist:
        file.writerow(line)
        e2.set()
        e1.wait()
        e1.clear()
def thread2(file,e2,e3):
    path = r"C:\Users\xuhao_yang\PycharmProjects\day21\csv\000002.csv"
    reader = csv.reader(open(path, "r"))
    alllist = []
    for item in reader:
        alllist.append(item)
    for line in alllist:
        e2.wait()
        e2.clear()
        file.writerow(line)
        e3.set()
def thread3(file,e3,e1):
    path = r"C:\Users\xuhao_yang\PycharmProjects\day21\csv\000003.csv"
    reader = csv.reader(open(path, "r"))
    alllist = []
    for item in reader:
        alllist.append(item)
    for line in alllist:
        e3.wait()
        e3.clear()
        file.writerow(line)
        e1.set()


file=csv.writer(open("1.csv","w",newline=""),dialect=("excel"))
e1=threading.Event()
e2=threading.Event()
e3=threading.Event()
threading.Thread(target=thread1,args=(file,e1,e2)).start()
threading.Thread(target=thread2,args=(file,e2,e3)).start()
threading.Thread(target=thread3,args=(file,e3,e1)).start()

file.close