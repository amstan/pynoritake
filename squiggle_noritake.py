#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import noritake
from squiggle import Squiggle
import numpy
import time

class NoritakeSquiggle(noritake.Display,Squiggle):
	"""Inspiration: https://www.youtube.com/watch?v=nxFad7Rxw7Q&t=0m44s"""
	empty_cell=numpy.zeros((8, 5))
	filled_cell=numpy.ones((8, 5))
	
	def split(self,frame):
		return numpy.array(numpy.split(numpy.array(numpy.split(frame,self.width,axis=-1)),self.height,axis=-2))
	
	def display(self):
		characters=self.split(self.storage)
		
		self.goto(0,0)
		for y,row in enumerate(characters):
			for x,cell in enumerate(row):
				#self.goto(x,y)
				if numpy.array_equal(self.empty_cell,cell):
					try:
						del self.cache[(x,y)]
					except KeyError:
						pass
					self.write(" ")
				else:
					cell=cell!=0
					
					try:
						#maybe this block used a special_char before
						special_char=self.cache[(x,y)]
					except KeyError:
						try:
							#new block, pick a new special_char
							special_char=tuple(self.custom_characters_available-set(self.cache.values()))[0]
						except IndexError:
							#print("Too many chars.")
							self.write(" ")
							continue
					
					self.define_custom_char(special_char,cell>0)
					self.serial.write(bytes([special_char]))
					self.cache[(x,y)]=special_char
					special_char+=1
	
	def __init__(self,serial,width,height):
		Squiggle.__init__(self,width=width*5,height=height*8,length=100)
		noritake.Display.__init__(self,serial,width,height)
		self.set_cursor_style(noritake.cursors["None"])
		self.custom_chars_enabled=True
		
		for i in range(0x20,0xff):
			self.delete_custom_char(i)
		
		self.cache={}
		special_char_start=ord("a")
		self.custom_characters_available={special_char_start+i for i in range(16)}
		
		#self.define_custom_char(" ",self.filled_cell>0)

if __name__=="__main__":
	import serial
	import time
	
	n=NoritakeSquiggle(
		serial.Serial("/dev/ttyUSB0",38400),
		24, 6
	)
	
	while(1):
		for i in range(1):
			n.step()
		n.display()