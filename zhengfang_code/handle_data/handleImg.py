# -*- coding: utf-8 -*-
# @Date    	: 2016-04-10 14:14:32
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com

from PIL import Image
class handleImg(object):
    def __init__(self,im): #the format of im must be PNG
        self.im=im
    
    #the color of code will be 255,white   
    def modifyFontColor(self,font=255,other=0):
        for x in range(self.im.width):
            for y in range(self.im.height):
                if self.im.getpixel((x,y))==255:
                    self.im.putpixel((x,y),other)
                else:
                    self.im.putpixel((x,y),font)
    '''
    check isolated point and delete it!    
    delete point by the round 8 points of the center point 
    t is the threshold of num
    colorValue is the threshold of the true font color value
    
    it will operating as if round count<=self.trueNum then delete it!
    and if colorValue
    ''' 
    def deletePointByNum(self,t=3,colorValue=100):
        for x in range(self.im.width):
            for y in range(self.im.height):
                if x!=0 and y!=0 and y!=self.im.height-1 and x!=self.im.width-1:
                    count=0
                    for i in range(-1,2):
                        for j in range(-1,2):
                            tx=x+i
                            ty=y+j
                            if self.im.getpixel((tx,ty))<colorValue:
                                count+=1
                    if count<=t:
                        self.im.putpixel((x,y),255) #isolated point and set white
    
    #delePointByColor has the same to deletePointByNum and it will be executed before that
    def delePointByColor(self,colorValue=100):
        for x in range(self.im.width):
            for y in range(self.im.height):
                if self.im.getpixel((x,y))>colorValue:
                    self.im.putpixel((x,y),255)                   
    
    #combine delePointByColor and deletePointByNum
    def isolatedPoint(self):
        self.delePointByColor()
        self.deletePointByNum()
        
    #set edge color value for 255 white
    def handleEdgeIfNeed(self):
        for x in range(self.im.width):
            self.im.putpixel((x,0),255)
            self.im.putpixel((x,self.im.height-1),255)
        for y in range(self.im.height):
            self.im.putpixel((0,y),255)
            self.im.putpixel((self.im.width-1,y),255)
    
    #the door of class finally it will return image object
    def handle(self):
        self.handleEdgeIfNeed()
        self.isolatedPoint()
        self.modifyFontColor()
        return self.im