# -*- coding: utf-8 -*-
# @Date    	: 2016-04-10 14:14:24
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com
import os,sys,time
__file__ = os.path.abspath(__file__)
if os.path.islink(__file__):
    __file__ = getattr(os, 'readlink', lambda x: x)(__file__)

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
from handleImg import handleImg
from splitImg import splitImg

from PIL import Image

def main(img_path):
		im=Image.open(img_path)
		hi=handleImg(im)
		im=hi.handle()
		si=splitImg(im)
		return si.split()

if __name__=='__main__':
	print(main('D:\\workspace\\python\\recognition_verify_code\\zhengfang_code\\img\\download\\0.png'))

