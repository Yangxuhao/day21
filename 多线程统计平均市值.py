import csv
import threading
import queue
import os

myqueue=queue.Queue(0)

class getdatatotal(threading.Thread):
    def __init__(self,path,queue):
        threading.Thread.__init__(self)
        self.path=path
        self.queue=queue

    def run(self):
        print("start",self.getName())
        reader = csv.reader(open(path, "r"))
        num = 0
        alldata = 0
        for item in reader:
            if num == 0:
                pass
            else:
                adddata = eval(item[13])
                alldata += adddata
            num += 1
        print(alldata / num,self.getName())
        self.queue.put(alldata / num)

if __name__=="__main__":
    path=r"C:\Users\xuhao_yang\PycharmProjects\day21\csv"
    filelist=os.listdir(path)
    filepathlist=[]
    for i in filelist:#生成每个文件的路径
        filepathlist.append(path+"\\"+i)

    threadlist=[]
    for path in filepathlist:
        mythd=getdatatotal(path,myqueue)
        mythd.start()
        threadlist.append(mythd)
    for thd in threadlist:
        thd.join()
    while not myqueue.empty():
        data=myqueue.get()
        print(data)
