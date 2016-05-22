# -*- coding:utf-8 -*-

import queue,os,sys
import threading
from urllib import request
import urllib
import hashlib

PATH=os.path.join(sys.path[0],'img')
MULTI_THREADING=5

CODE_URL='http://www.stu1314.com/validata_code.aspx'
IMG_NUM=10

img_md5={}
class imgThread(threading.Thread):
    def __init__(self,qe):
        threading.Thread.__init__(self)
        self.qe=qe
    def run(self):
        global img_md5
        while True:
            sid=self.qe.get()
            #try:
            f=urllib.request.urlopen(CODE_URL, timeout=3).read()
            with open(os.path.join(PATH,str(sid)+'.png'),'wb') as fw:
                m=hashlib.md5(f).hexdigest()
                if m in img_md5:
                    self.qe.put(sid)
                    print(sid,'md5 value has appeared!')
                else:
                    fw.write(f)
                    img_md5[m]=True
                    print('finished download the',str(sid),'image and md5 Value:',hashlib.md5(f).hexdigest())
            #except:
                #self.qe.put(sid)
                #print('download fail')
            self.qe.task_done()

def download():
    qe=queue.Queue()
    for i in range(MULTI_THREADING):
        t=imgThread(qe)
        t.setDaemon(True)
        t.start()
    for i in range(IMG_NUM):
        qe.put(i)

    qe.join()

if __name__=='__main__':
    download()
