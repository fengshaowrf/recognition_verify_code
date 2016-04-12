# -*- coding: utf-8 -*-
# @Date     : 2016-04-11 23:06:35
# @Author   : mr0cheng
# @email    : c15271843451@gmail.com

from numpy import genfromtxt
from PIL import Image
from sklearn import neighbors, datasets
import numpy as np

N_NEIGHBORS = 15

class predict(object):
    clf=''
    def __init__(self):
        pass

    def train(self,csv_path):
        train_data = genfromtxt(csv_path, delimiter=' ')
        x=train_data[:,:400]
        y=train_data[:,400]
        
        self.clf = neighbors.KNeighborsClassifier(N_NEIGHBORS, weights='distance')
        self.clf.fit(x, y)

    def predict(self,im):
        temp=[]
        for x in range(im.width):
            for y in range(im.height):
                if im.getpixel((x,y)):
                    temp.append(1)
                else:
                    temp.append(0)
        return chr(int(self.clf.predict(np.array(temp))[0]))   