# -*- coding: utf-8 -*-
# @Date    	: 2016-04-10 14:17:53
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com

# -*- coding:utf-8 -*-
from PIL import Image 
from rotateImg import rotateImg
class splitImg:
    im1=''
    im2=''
    im3=''
    im4=''
    color=[]
    ori=0
    tar=0
    dmin=3
    dmax=16
    dmean=9
    def __init__(self,im):
        self.im=im
        self.color=[]
    def getColorList(self,colorValue):
        cl=[]
        for x in range(self.im.width):
            for y in range(self.im.height):
                xy=tuple((x,y))
                if self.im.getpixel(xy)==colorValue:
                    cl.append(xy)
        return cl
    #correct the image cfs
    def isHaveIJ(self):
        tempcolor=[]
        for i in self.color:
            colorList=self.getColorList(i)
            if len(colorList)<8 and len(colorList)!=0:
                for c in colorList:
                    x=c[0]
                    for y in range(self.im.height):
                        p=self.im.getpixel((x,y))
                        if p!=i and p!=0:
                            self.ori=p
                            self.tar=i
                            self.fillColorByRecursive((x,y))
        for i in self.color:
            if len(self.getColorList(i))==0:
                tempcolor.append(i)
        for i in tempcolor:
            self.color.remove(i)
            
    #modify ori color--->tar color 
    def fillColorByRecursive(self,xy):
        self.im.putpixel(xy,self.tar)
        for i in range(-1,2):
            for j in range(-1,2):
                tx=xy[0]+i
                ty=xy[1]+j
                if self.im.getpixel((tx,ty))==self.ori:
                    self.fillColorByRecursive((tx,ty))
    #Color filling segmentation  
    def cfs(self):
        cc=0
        for x in range(self.im.width):
            for y in range(self.im.height):
                if self.im.getpixel((x,y))==255:
                    cc+=1
                    self.color.append(cc)
                    self.ori=255
                    self.tar=cc
                    self.fillColorByRecursive((x,y))
                    break
        #set i j for same color and return the true color's number
        self.isHaveIJ()
    def getBBBBBox(self):
        boxes=[]
        if len(self.color)==1:
            box=tuple((0,0,self.im.width,self.im.height))
            boxes.append(box)
        else:
            for i in self.color:
                top=0
                bot=0
                for x in range(self.im.width):
                    flag=0
                    for y in range(self.im.height):
                        if self.im.getpixel((x,y))==i:
                            flag=1
                            break
                    if flag:
                        if top==0:
                            top=x
                        bot=x
                    elif top:
                        box=(top,0,bot+1,self.im.height-1)
                        boxes.append(box)
                        break
        return boxes
    
    #start to split picture by color filling segemetation
    def startSplit(self,boxes):
        a=[]
        for i in range(4):
            tm=self.im.crop(boxes[i])
            if tm.width>20:
                return False
            for tx in range(tm.width):
                for ty in range(tm.height):
                    if tm.getpixel((tx,ty))==self.color[i]:
                        tm.putpixel((tx,ty),255)
                    else:
                        tm.putpixel((tx,ty),0)
            rt=rotateImg(tm)
            tm=rt.rotate()
            a.append(tm)
        return a
    
    def FlagAndWater(self,box,color,times):
        if times==0:
            return
        tm=self.im.crop(box)
        path=self.dropWater(tm,color,self.getFlagForDropWater(tm,color))
        recolor=0
        for c in self.color:
            if c>recolor:
                recolor=c
        recolor+=1
        self.color.insert(self.color.index(color)+1,recolor)
        maxX=0  #get the max width of has gotten character.because if its behind char has been same colored if max got bigger
                #it will be affectness
        for tp in path:
            if tp[0]>maxX:
                maxX=tp[0]
            for x in range(box[0]+tp[0],box[2]):
                if tm.getpixel((x-box[0],tp[1]))==color:
                    self.im.putpixel((x,tp[1]),recolor)
        #print(box)
        box=tuple((maxX+box[0],0,box[2],self.im.height))
        times-=1
        self.FlagAndWater(box,recolor,times)
        return 
    #if cfs < 4 , will sort and get four color    
    def sortBoxes(self,boxes):
        if len(boxes)==1:
            self.FlagAndWater(boxes[0],self.color[0],3)
        elif len(boxes)==2:
            a1=boxes[0][2]-boxes[0][0]
            a2=boxes[1][2]-boxes[1][0]
            if abs(a1-a2)<self.dmin*3:
                self.FlagAndWater(boxes[0],self.color[0],1)
                self.FlagAndWater(boxes[1],self.color[1],1)
            elif a1>a2:
                self.FlagAndWater(boxes[0],self.color[0],2)
            else:
                self.FlagAndWater(boxes[1],self.color[1],2)
        else:
            a1=boxes[0][2]-boxes[0][0]
            a2=boxes[1][2]-boxes[1][0]
            a3=boxes[2][2]-boxes[2][0]
            if a1>a2 and a1>a3:
                self.FlagAndWater(boxes[0],self.color[0],1)
            elif a2>a1 and a2>a3:
                self.FlagAndWater(boxes[1],self.color[1],1)
            else:
                self.FlagAndWater(boxes[2],self.color[2],1)
    '''
    only handle hte easy image
    '''
    def split(self):
        self.cfs()
        boxes=self.getBBBBBox()
        if len(boxes)==4:
            return self.startSplit(boxes)
        return False
        

                

