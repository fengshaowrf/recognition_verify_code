from PIL import Image
import sys,os
import handle


PATH=sys.path[0]
BGC=255
FONT=0


BLOCK_T=40
def delete_block(im):
    color=1
    for x in range(im.width):
        for y in range(im.height):
            if im.getpixel((x,y))==0:
                handle.fillColorByRecursive(im,color,(x,y),FONT)
                color+=1

    dic={}
    dic[255]=0
    for i in range(1,color+1):
        dic[i]=0

    for x in range(im.width):
        for y in range(im.height):
            dic[im.getpixel((x,y))]+=1

    rml={}
    for i in range(1,color+1):
        if dic[i]<BLOCK_T:
            rml[i]=True

    for x in range(im.width):
        for y in range(im.height):
            if im.getpixel((x,y)) in rml:
                im.putpixel((x,y),BGC)

THRE=5      #if the number of font is more than 5,end.
def delete_line(im):
    line=[]

    visit=[[0 for y in range(im.height)] for x in range(im.width)]
    for x in range(im.width):
        for y in range(im.height):
            if im.getpixel((x,y))==FONT:
                count=0
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if im.getpixel((x+i,y+j))==FONT:
                            count+=1
                if count<2 or count>4:
                    visit[x][y]=1
            else:
                visit[x][y]=1
    for x in range(im.width):
        for y in range(im.height):
            if visit[x][y]!=0 and im.getpixel((x,y))==FONT:
                state,newline=handle.match_line(im,(x,y),THRE,visit,BGC)
                if state:
                    line.append(newline)


def handle_edge(im):
    handle.handle_edge(im,255)

def grey(im,img_name):
    cur_folder=os.path.join(PATH,'grey')
    im.save(os.path.join(cur_folder,img_name))

def delete_point(im,img_name):
    cur_folder=os.path.join(PATH,'delete_point')
    handle.move_isolated(im,1,255,3)

def print_pixel(im):
    for x in range(im.width):
        p=[]
        for y in range(im.height):
            p.append(im.getpixel((x,y)))
        print(p)
def main():
    cur_folder=os.path.join(PATH,'img')
    for i in range(10):
        im=Image.open(os.path.join(cur_folder,str(i)+'.png'))
        im=im.convert('L')
        handle.black_white(im,180)
        handle_edge(im)
        delete_block(im)
        handle.black_white(im,BGC)

        #delete_line(im)
        #handle.black_white(im,BGC)
        im.save(str(i)+'.png')

if __name__=='__main__':
    main()
