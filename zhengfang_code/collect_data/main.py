# -*- coding: utf-8 -*-
# @Date    	: 2016-04-10 10:09:35
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com
import os,sys,time
__file__ = os.path.abspath(__file__)
if os.path.islink(__file__):
    __file__ = getattr(os, 'readlink', lambda x: x)(__file__)

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
from downloadImg import download
url='http://jw.hzau.edu.cn/CheckCode.aspx?'

def main(img_num,path):
	st=time.time()
	download(img_num,path,url)
	print('DONE!!!total time :',time.time()-st)