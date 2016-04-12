# -*- coding: utf-8 -*-
# @Date    	: 2016-04-11 23:18:27
# @Author  	: mr0cheng
# @email	: c15271843451@gmail.com

import os,sys,time
__file__ = os.path.abspath(__file__)
if os.path.islink(__file__):
    __file__ = getattr(os, 'readlink', lambda x: x)(__file__)

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

from predict import predict

def main(csv_path,img_list):
	p=predict()
	p.train(csv_path)
	result=''
	for i in img_list:
		result+=p.predict(i)
	return result