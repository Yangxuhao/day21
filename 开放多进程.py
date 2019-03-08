import multiprocessing
import os


def findkaifang(kaifanglist,istart,iend,searchstr,lastlist):
    for i in range(istart,iend):
        line=kaifanglist[i].decode("gbk","ignore")
        if line.find(searchstr)!=-1:
            print(line)
            lastlist.append(line)

def loaddata():
    path = r"D:\尹成python\kaifangx.txt"
    with open(path, "rb") as file:
        global kaifanglist
        kaifanglist.extend(file.readlines())

if __name__=="__main__":
    kaifanglist = multiprocessing.Manager().list()
    lastlist = multiprocessing.Manager().list()
    loaddata()
    datalength=len(kaifanglist)
    N=10#开启十个进程
    processlist=[]
    findstr=input("input")
    for i in range(0,N-1):#前九个进程平分数据
        myprocess=multiprocessing.Process(target=findkaifang,args=(kaifanglist,
                                                                   i*(datalength//(N-1)),
                                                                   (i+1)*(datalength//(N - 1)),
                                                                   findstr,
                                                                   lastlist
                                                                    ))
        myprocess.start()
        processlist.append(myprocess)
    mylastprocess=multiprocessing.Process(target=findkaifang,args=(kaifanglist,
                                                                   (N-1)*(datalength//(N-1)),
                                                                   datalength,
                                                                   findstr,
                                                                   lastlist
                                                                    ))
    #最后一个进程处理剩余的数据
    mylastprocess.start()
    processlist.append(mylastprocess)

    for process in processlist:
        process.join()

    file=open("last.txt","wb")
    for line in lastlist:
        file.write(line.encode("utf-8"))
    file.close()