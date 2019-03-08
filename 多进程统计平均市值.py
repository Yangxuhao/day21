import csv
import multiprocessing
import os

def gettotal(path,queue):
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
    queue.put(alldata/num)




if __name__=="__main__":
    queue=multiprocessing.Queue()
    path=r"C:\Users\xuhao_yang\PycharmProjects\day21\csv"
    filelist=os.listdir(path)
    filepathlist=[]
    for i in filelist:#生成每个文件的路径
        filepathlist.append(path+"\\"+i)

    myprolist=[]
    for filepath in filepathlist:
        p=multiprocessing.Process(target=gettotal,args=(filepath,queue))
        p.start()
        myprolist.append(p)
    for item in myprolist:
        item.join()
    while not queue.empty():
        data=queue.get()
        print(data)



