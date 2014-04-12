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
	def __init__(self,width,height,length=50):
		self.length=length
		self.size=numpy.array([height,width])
		
		self.point=numpy.array([
			random.randint(0,self.size[0]),
			random.randint(0,self.size[1]),
		])
		
		self.storage=numpy.zeros((height,width))
		self.step()
	
	def sparkle(self,age,reach,count):
		try:
			point=numpy.argwhere(self.storage==age)[0]
		except IndexError:
			return
		self.storage[tuple(point)]=0
		
		for i in range(count):
			d=numpy.random.randint(-reach,reach,size=(2))
			#print d,reach
			newpoint=(point+d) % self.size
			self.storage[tuple(newpoint)]=age
	
	def clear(self,age,count):
		points=numpy.argwhere(self.storage==age)
		
		for i in range(min(count,len(points))):
			self.storage[tuple(random.choice(points))]=0
	
	def step(self):
		#advance age
		blanks=self.storage==0
		blanks|=self.storage>self.length
		self.storage+=1
		self.storage[blanks]=0
		
		#draw more of the line
		new_positions=[(self.point+choice)%self.size for choice in directions]
		non_crowded_positions=[pos for pos in new_positions if self.storage[tuple(pos)]==0]
		if non_crowded_positions:
			self.point=random.choice(non_crowded_positions)
		else:
			self.point=random.choice(new_positions)
		
		self.storage[tuple(self.point)]=1
		
		for i in range(int(self.length*0.2),int(self.length*0.8)):
			if(random.random()<0.004):
				self.sparkle(i,reach=5,count=2)
		for i in range(int(self.length*0.8),int(self.length*1.0)):
			if(random.random()<0.04):
				self.clear(i,count=1)

if __name__=="__main__":
	import time
	
	s=Squiggle(
		width=24*5,
		height=6*8,
	)
	
	def test():
		import matplotlib.pyplot as plt
		import matplotlib.animation
		fig = plt.figure()
		ax = plt.axes(xlim=(0, s.size[1]), ylim=(0, s.size[0]))
		im=plt.imshow(s.storage,interpolation='none')
		
		# animation function.  This is called sequentially
		def animate(i):
			s.step()
			im.set_array(s.storage/s.length)
			print("step")
			return [im]
		
		anim = matplotlib.animation.FuncAnimation(fig, animate, frames=None, interval=30, blit=True)
		plt.show()
	test()