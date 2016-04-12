# -*- coding:utf-8 -*-

import queue,os
import threading
from urllib import request
import urllib
import hashlib

MULTI_THREADING=50

CODE_URL=''
count=0

img_md5={}
class imgThread(threading.Thread):
    def __init__(self,qe,path):
        threading.Thread.__init__(self)
        self.qe=qe
        self.path=path
    def run(self):
        global count
        global img_md5
        while True:
            sid=self.qe.get()
            try:
                f=urllib.request.urlopen(CODE_URL, timeout=3).read()
                with open(os.path.join(self.path,str(sid)+'.png'),'wb') as fw:
                    m=hashlib.md5(f).hexdigest()
                    if m in img_md5:
                        self.qe.put(sid)
                        print(sid,'md5 value has appeared!')
                    else:
                        fw.write(f)
                        img_md5[m]=True
                        count+=1
                        print('finished download the',count,'image and md5 Value:',hashlib.md5(f).hexdigest())
            except:
                self.qe.put(sid)
                print('download fail')
            self.qe.task_done()
'''
img         :the number of download img
path        :the image path
'''
def download(img_num,path,code_url):
    global CODE_URL
    CODE_URL=code_url
    qe=queue.Queue()
    for i in range(MULTI_THREADING):
        t=imgThread(qe,path)
        t.setDaemon(True)
        t.start()
    for i in range(img_num):
        qe.put(i)
    
    qe.join()
    
if __name__=='__main__':
    worker(50, 200)
    
                
            