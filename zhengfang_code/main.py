# -*- coding: utf-8 -*-
# @Date     : 2016-04-10 10:19:02
# @Author   : mr0cheng
# @email    : c15271843451@gmail.com

import os,sys
import hashlib
from PIL import Image
import collect_data.main as cm
import handle_data.main as hm
import knn_predict.main as km
import numpy as np
import csv

DL_IMG_FOLDER=os.path.join(sys.path[0],'img','download')
NUM_CHAR_FOLDER=os.path.join(sys.path[0],'img','1_9a_z')

CSV_FILE=os.path.join(sys.path[0],'train.csv')

def clearRepeat(flist):
    f_md5={}
    for i in flist:
        with open(os.path.join(FOUR_IMG_FOLDER,i),'rb') as fr:
            fr=fr.read()
            m=hashlib.md5(fr).hexdigest()
            if m not in f_md5:
                f_md5[m]=[]
            f_md5[m].append(i)

    for i in f_md5:
        if len(f_md5[i])>1:
            print(f_md5[i])

    for i in f_md5:
        if len(f_md5[i])>1:
            for j in range(1,len(f_md5[i])):
                os.remove(os.path.join(FOUR_IMG_FOLDER,f_md5[i][j]))

def imgToCSV():
    flist=os.listdir(NUM_CHAR_FOLDER)
    features=[]
    for i in flist:
        subflist=os.listdir(os.path.join(NUM_CHAR_FOLDER,i))
        for j in subflist:
            temp=[]
            im=Image.open(os.path.join(NUM_CHAR_FOLDER,i,j))
            for x in range(im.width):
                for y in range(im.height):
                    if im.getpixel((x,y)):
                        temp.append(1)
                    else:
                        temp.append(0)
            temp.append(ord(i))
            features.append(temp)

    with open(CSV_FILE,'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ')
        for i in features:
            spamwriter.writerow(i)
def collect_data(img_num):
    cm.main(img_num,DL_IMG_FOLDER)
def work(csv_path,img_path):
    r=hm.main(img_path)
    if r is not False:
        print('result:',km.main(csv_path,r))
    else:
        print('fail to work')
if __name__=='__main__':
    flist=os.listdir(DL_IMG_FOLDER)
    for i in flist:
        work(os.path.join(sys.path[0],'train.csv'),os.path.join(DL_IMG_FOLDER,i))
#17 3 9.375
#20 10 14.5307377049
#20 20