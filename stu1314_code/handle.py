import os,sys
from PIL import Image

''';
this way can only afford to appear once the one point in a line.
'''
def getxy(im,xy,bgc):
    x=0
    y=0
    tx=xy[0]
    ty=xy[1]
    if im.getpixel((xy[0],xy[1]+1))!=bgc:
        x=0
        y=1
        tx,ty,line=until_to_end(im,xy,x,y,bgc)
    elif im.getpixel((xy[0]+1,xy[1]))!=bgc:
        x=1
        y=0
        tx,ty,line=until_to_end(im,xy,x,y,bgc)

    if x==0 and y==0:
        if im.getpixel((tx+1,ty-1))!=bgc:
            x=1
            y=0
        elif im.getpixel((tx+1,ty+1))!=bgc:
            if im.getpixel((tx+2,ty+1))!=bgc:
                x=1
                y=0
            elif im.getpixel((tx+1,ty+2))!=bgc:
                x=0
                y=1
        elif im.getpixel((tx-1,ty+1))!=bgc:
            x=0
            y=1
    return (x,y)

def getqxy(im,xy,bgc):
    qx=0
    qy=0
    tx,ty=xy
    if im.getpixel((tx+1,ty-1))!=bgc:
        qx=1
        qy=-1
    elif im.getpixel((tx+1,ty+1))!=bgc:
        qx=1
        qy=1
    elif im.getpixel((tx-1,ty+1))!=bgc:
        qx=-1
        qy=1
    return (qx,qy)

def until_to_end(im,xy,x,y,bgc):
    tx,ty=xy
    line=[]
    while im.getpixel((tx+x,ty+y))!=bgc:
        tx+=x
        ty+=y
        line.append((tx,ty))
    return (tx,ty,line)

'''
im:image handler
xy:the tuple of x,y
'''
def match_line(im,xy,thre,visit,bgc):
    line=[]
    line.append(xy)
    x,y=getxy(im,xy,bgc)     #horization or column
    qx,qy=getqxy(im,xy,bgc)  #/\or /
    if qx==0 and qy==0:
        qx=x
        qy=y

    if x==0 and y==0:
        tx,ty=xy
        while im.getpixel((tx,ty))!=bgc:
            line.append((tx,ty))
            tx+=1
            ty+=1
    else:
        tx,ty,exline=until_to_end(im,xy,x,y,bgc)
        line.extend(exline)
        while im.getpixel((tx+qx,ty+qy))!=bgc:
            line.append((tx+qx,ty+qy))
            tx,ty,exline=until_to_end(im,(tx+qx,ty+qy),x,y,bgc)
            line.extend(exline)

    for i in line:
        count=0
        for x in range(-1,2):
            for y in range(-1,2):
                if im.getpixel((i[0]+x,i[1]+y))!=bgc:
                    count+=1
        if count<5:
            im.putpixel(i,bgc)
        else:
            break






'''
get the histogram about the number of font pixel in every column.

im:image handler
bgc:background color
'''
def his_col(im,bgc):
    p=[0 for y in range(im.width)]
    for x in range(im.width):
        for y in range(im.height):
            if im.getpixel((x,y))!=bgc:
                p[x]+=1
    return p

'''
fill the same color if it's connceted.

im:image handler
color:which color will be filled
xy:the tuple of x,y
bgc:background color
'''
def fillColorByRecursive(im,color,xy,font):
    im.putpixel(xy,color)
    for i in range(-1,2):
        for j in range(-1,2):
            tx=xy[0]+i
            ty=xy[1]+j
            if tx==-1 or ty==-1 or tx==im.width or ty==im.height:
                continue
            if im.getpixel((tx,ty))==font:
                fillColorByRecursive(im,color,(tx,ty),font)
'''
binaryzation,font is black,bgc is white.Or oppsitively.

im:image handler
t:the threshold to decide if it is bgc.
'''
def black_white(im,t):
    for x in range(im.width):
        for y in range(im.height):
            if im.getpixel((x,y))>=t:
                im.putpixel((x,y),255)
            else:
                im.putpixel((x,y),0)

'''
set edge to white
'''
def handle_edge(im,bgc):
    for x in range(im.width):
        im.putpixel((x,0),bgc)
        im.putpixel((x,im.height-1),bgc)
    for y in range(im.height):
        im.putpixel((0,y),bgc)

'''
handle line,the line has a charcater for straight line.

im:image handler
visit:visit list
xy:the tuple of x,y
bgc:background color
'''
def delete_line(im,visit,xy,bgc):
    '''
    demo:
        On the high side,has the point value must be equal 0 among (x+1,y),(x+1,y-1) and (x,y-1).
        On the low side,has the point value must be equal 0 among (x+1,y),(x+1,y+1) and (x,y-1).
    '''
    return im

'''
im:image handler
num:the threshold
bgc:background color
w:the width of square
'''
def move_isolated(im,num,bgc,w):
    for x in range(w//2,im.width-1-w//2):
        for y in range(w//2,im.height-1-w//2):
            count=0
            if im.getpixel((x,y))!=bgc:
                for i in range(-1*(w//2),w//2+1):
                    for j in range(-1*(w//2),w//2+1):
                        if im.getpixel((x+i,y+j))!=bgc:
                            count+=1
            if count<=num+1:
                im.putpixel((x,y),bgc)
    return im
