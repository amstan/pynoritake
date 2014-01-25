#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import noritake
from squiggle import Squiggle
import numpy

class NoritakeSquiggle(noritake.Display,Squiggle):
	empty_cell=numpy.zeros((8, 5))
	filled_cell=numpy.ones((8, 5))
	def split(self,frame):
		return numpy.array(numpy.split(numpy.array(numpy.split(frame,self.width,axis=-1)),self.height,axis=-2))
	
	def display(self):
		characters=self.split(numpy.sum(self.storage,axis=0))
		
		special_char_start=ord("a")
		
		self.goto(0,0)
		special_char=0
		for y,row in enumerate(characters):
			for x,cell in enumerate(row):
				if numpy.array_equal(self.empty_cell,cell):
					self.write(" ")
				else:
					if special_char==16:
						print("Too many chars.")
						continue
					cell=cell!=0
					self.define_custom_char(special_char_start+special_char,cell>0)
					self.serial.write(bytes([special_char_start+special_char]))
					special_char+=1
	
	def __init__(self,serial,width,height):
		Squiggle.__init__(self,width=width*5,height=height*8,length=200)
		noritake.Display.__init__(self,serial,width,height)
		self.set_cursor_style(noritake.cursors["None"])
		self.custom_chars_enabled=True
		
		for i in range(0x20,0xff):
			self.delete_custom_char(i)
		
		#self.define_custom_char(" ",self.filled_cell>0)

if __name__=="__main__":
	import serial
	import time
	
	n=NoritakeSquiggle(
		serial.Serial("/dev/ttyUSB0",38400),
		24, 6
	)
	
	while(1):
		for i in range(10):
			n.step()
		n.display()
		#time.sleep(0.1)