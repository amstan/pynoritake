#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import numpy
import random

directions=[
	[0,0],
	
	[0,-1],
	[1,-1],
	[1,0],
	[1,1],
	[0,1],
	[-1,1],
	[-1,0],
	[-1,-1],
]

class Squiggle(object):
	def __init__(self,width,height,length=400):
		self.length=length
		self.size=numpy.array([height,width])
		
		self.point=numpy.array([
			random.randint(0,self.size[0]),
			random.randint(0,self.size[1]),
		])
		
		self.storage=numpy.zeros((length,height,width))
		self.step()
	
	def sparkle(self,frame,reach=10,count=1):
		try:
			point=numpy.argwhere(frame>0)[0]
		except IndexError:
			return
		frame[tuple(point)]=0
		
		for i in range(count):
			d=numpy.random.randint(-reach,reach,size=(2))
			#print d,reach
			newpoint=(point+d) % self.size
			frame[tuple(newpoint)]=1
	
	def clear(self,frame,count=1):
		points=numpy.argwhere(frame>0)
		
		for i in range(min(count,len(points))):
			frame[tuple(random.choice(points))]=0
	
	def step(self):
		self.storage=numpy.roll(self.storage,-1,axis=0)
		self.storage[-1]=numpy.zeros_like(self.storage[0])
		
		self.point+=random.choice(directions)
		#self.point+=[1,1]
		self.point%=self.size
		
		for i in range(int(self.storage.shape[0]*0.2),int(self.storage.shape[0]*0.7)):
			if(random.random()<0.001):
				self.sparkle(self.storage[i],reach=6,count=2)
		for i in range(0,int(self.storage.shape[0]*0.8)):
			if(random.random()<0.02):
				self.clear(self.storage[i])
		
		self.storage[-1][tuple(self.point)]=2

	def simplecv_display(self):
		import SimpleCV
		todisplay=numpy.zeros_like(self.storage[0])
		n=len(self.storage)
		for i,frame in enumerate(self.storage):
			frame=frame>0
			todisplay+=frame*((i/(n-1))*255)
			#todisplay+=frame*255
		todisplay=numpy.transpose(todisplay)
		todisplay=numpy.clip(todisplay,0,255)
		SimpleCV.Image(todisplay).scale(5,interpolation=SimpleCV.cv2.INTER_NEAREST).show()

if __name__=="__main__":
	import time
	
	s=Squiggle(
		width=24*5,
		height=6*8,
	)
	
	while 1:
		s.simplecv_display()
		for i in range(10):
			s.step()