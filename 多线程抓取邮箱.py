import urllib.request
import urllib
import re
import threading
import queue
import time

def getdata(url):
    try:
        data=urllib.request.urlopen(url).read().decode("utf-8")
        return data
    except:
        return ""

def getemail(data):
    maileregx = re.compile("([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})", re.IGNORECASE)
    try:
        mylist = maileregx.findall(data)
        return mylist
    except:
        return []
def gethttp(data):
    httpregx = re.compile(r"(http://\S*?)[\"|\)]", re.IGNORECASE)
    try:
        mylist = httpregx.findall(data)
        return mylist
    except:
        return []

def getabsUrl(url,data):#相对路径
    try:
        listUrl=[]
        regex=re.compile("href=\"(.*?)\"",re.IGNORECASE)
        httplist=regex.findall(data)
        newhttplist=httplist.copy()
        hostname=gethostname(url)
        for data in newhttplist:
            if data.find("http://")!=-1:
                httplist.remove(data)
            elif data.find("javascript")!=-1:
                httplist.remove(data)
        if hostname!=None:
            for i in range(len(httplist)):
                httplist[i]=hostname+httplist[i]
        return httplist
    except:
        return []
def gethostname(httpstr):
    httpregx = re.compile(r"(http://\S*?)/", re.IGNORECASE)
    try:
        mylist = httpregx.findall(httpstr)
        if len(mylist)==0:
            return None
        else:
            return mylist[0]
    except:
        return []
def getallUrl(data):
        mylist2=[]
        mylist=[]
        mylist = gethttp(data)
        if len(mylist)!=0:
            mylist2 = getabsUrl(mylist[0],data)
        alllist=[]
        alllist.extend(mylist)
        alllist.extend(mylist2)
        return alllist

# pagedata=getdata("http://bbs.tianya.cn/post-140-393974-2.shtml")
# # mylist=gethttp(pagedata)
# # # hostname=gethostname(mylist[0])
# # # print("hostname",hostname)
# # print("path",getabsUrl(mylist[0],pagedata))
# print(getallUrl(pagedata))


def BFSget(urlstr,myqueue):
    myqueue.put(urlstr)
    while not myqueue.empty():
        url = myqueue.get()
        print(url)
        pagedata = getdata(url)
        emaillist = getemail(pagedata)
        if len(emaillist) != 0:
            for mail in emaillist:
                print(mail)
        newurllist = getallUrl(pagedata)
        if len(newurllist) != 0:
            for urlstr in newurllist:
                # if urlstr not in myqueue:
                    myqueue.put(urlstr)

def newBFS(urlstr,myqueue):
    # print(urlstr)
    pagedata = getdata(urlstr)
    emaillist = getemail(pagedata)
    if len(emaillist) != 0:
        for mail in emaillist:
            print(mail)
            myqueue.put(mail)
    newurllist = getallUrl(pagedata)
    if len(newurllist) != 0:
        for urlstr in newurllist:
            with sem:
                threading.Thread(target=newBFS, args=(urlstr, myqueue)).start()


def BFS(urlstr,myqueue):
    with sem:
        threading.Thread(target=newBFS,args=(urlstr,myqueue)).start()
def saveemail():
    global  myqueue
    file=open("email.txt","wb")
    while True:
        time.sleep(5)
        while not myqueue.empty():
            data=myqueue.get()
            print(data)
            file.write((data+"\r\n").encode("utf-8"))
            file.flush()#实时写入
    file.close()


sem=threading.Semaphore(10)
myqueue=queue.Queue(0)
timethread=threading.Timer(5,saveemail)
timethread.start()
BFS("http://bbs.tianya.cn/post-140-393974-2.shtml",myqueue)