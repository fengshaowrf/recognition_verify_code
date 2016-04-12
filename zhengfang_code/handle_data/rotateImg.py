# -*- coding: utf-8 -*-
# @Date    	: 2016-04-10 14:40:13
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com
# -*- coding:utf-8 -*-

# -*- coding:utf-8 -*-
class rotateImg:
    def __init__(self,im):
        self.im=im
    
    def findMinimumLength(self):
        llist=[]
        for angle in range(45,-45,-1):
            box=self.im.rotate(angle,expand=1).getbbox()
            llist.append(box[2]-box[0])
        minW=self.im.width
        for i in range(len(llist)):
            if minW>llist[i]:
                minW=llist[i]
        count=0
        flag=0
        for i in range(len(llist)):
            if minW==llist[i]:
                count+=1
                flag+=i
        flag=int(flag/count)
        flag=45-flag
        if flag<0:
            flag+=1
        #print(llist)
        #print(flag)
        return flag
    def rotate(self):
        self.im=self.im.rotate(self.findMinimumLength(),expand=1)
        return self.im.crop(self.im.getbbox()).resize((20,20))
        