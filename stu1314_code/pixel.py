from PIL import Image

import os,sys


def a():
    return [1,2,3]

def b():
    c=[]
    c.extend(a())
    print(c)
if __name__=='__main__':
    b()
