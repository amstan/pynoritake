#!/usr/bin/env python3
# -*- coding: utf-8 -*-

screensavers = {
	"Power Off": 0,
	"Power On": 1,
	"All Dots Off": 2,
	"All Dots On": 3,
}

cursors = {
	"Underline": 0x13,
	"None":  0x14,
	"Block": 0x15,
	"Blinking Underline": 0x16,
}

def reverse_bits(x, n=8):
	result = 0
	for i in range(n):
		if (x >> i) & 1: result |= 1 << (n - 1 - i)
	return result

class Display(object):
	def __init__(self,serial,width,height):
		self.serial=serial
		
		self.width=width
		self.height=height
		
		self.clear_screen()
		self.power=True
	
	def _esc(self,cmd):
		self.serial.write(b"\x1b")
		self.serial.write(bytes((cmd,)))
	
	def _esc2(self,cmd,b):
		self._esc(cmd)
		self.serial.write(bytes((b,)))
	
	def _us(self,grp,cmd):
		self.serial.write(bytes((0x1f,0x28,grp,cmd)))
	
	def back(self):
		self.serial.write(b"\x08")
	
	def forward(self):
		self.serial.write(b"\x09")
	
	def home(self):
		self.serial.write(b"\x0b")
	
	def goto(self,x,y):
		if x>self.width or y>self.height:
			raise ValueError("Coords bigger than screen.")
		
		self.serial.write(b"\x1f\x24")
		self.serial.write(bytes((x,0,y,0)))
	
	#def delete_char(self):
		
	
	#def delete_line(self):
		
	
	#def insert_space(self):
		
	
	#def insert_line(self):
		
	
	def clear_screen(self):
		self.serial.write(b"\x0c")
	
	def blink(self,enabled=True,on_time=10,off_time=10,times=0):
		self._us(0x61,0x11)
		self.serial.write(bytes((enabled,on_time,off_time,times)))
	
	def screensaver(self,mode=screensavers["All Dots On"]):
		self._us(0x61,0x40)
		self.serial.write(bytes((mode,)))
	
	_power=False
	@property
	def power(self):
		return self._power
	@power.setter
	def power(self,power):
		self._power=power
		self._us(0x61, 0x40)
		self.serial.write(bytes((power,)))
	
	_brightness=0
	@property
	def brightness(self):
		return self._brightness
	@brightness.setter
	def brightness(self,level):
		self._brightness=level
		level//=25
		self.serial.write(bytes((0x1f,0x58,level)))
	
	def set_char_brightness(self,level=100):
		self._us(0x67,0x50)
		self.serial.write(bytes((level,0,0)))
	
	_custom_chars_enabled=False
	@property
	def custom_chars_enabled(self):
		return self._custom_chars_enabled
	@custom_chars_enabled.setter
	def custom_chars_enabled(self,enabled):
		_custom_chars_enabled=enabled
		self._esc(0x25)
		self.serial.write(bytes((enabled,)))
	
	custom_chars={}
	def define_custom_char(self,char,data):
		if isinstance(char,int):
			code=char
		else:
			code=ord(char)
		self.custom_chars[code]=data
		self._esc(0x26)
		newdata=[0]*5
		for row in range(8):
			for column in range(5):
				bit=row*5+column
				newdata[bit//8]|=(data[row][column])<<(bit%8)
		self.serial.write((0x01,code,code,5)+tuple(newdata))
	
	def delete_custom_char(self,char):
		if isinstance(char,int):
			code=char
		else:
			code=ord(char)
		self._esc2(0x3f,0x01)
		self.serial.write((code,))
	
	def display_custom_char(self,data):
		unused_chars=set(range(0x20,0xff))-self.custom_chars.keys()
		first_unused_char=chr(tuple(unused_chars)[0])
		self.define_custom_char(first_unused_char,data)
		self.write(first_unused_char)
	
	def set_cursor_style(self,style=cursors["Blinking Underline"]):
		self.serial.write(bytes((style,)))
	
	def write(self,string):
		string=string.replace("\n","\n\r")
		self.serial.write(string.encode("ascii"))

def booleanize(string):
	string=string.replace("\t","").strip("\n\r")
	data=[]
	for row,line in enumerate(string.split("\n")):
		data.append([char!=" " for char in line])
	return data

if __name__=="__main__":
	import serial
	import sys
	import datetime
	import time
	import random
	import math
	
	n=Display(
		serial.Serial("/dev/ttyUSB0",38400),
		24, 6
	)
	n.set_cursor_style(cursors["None"])
	
	n.brightness=100
	
	n.set_char_brightness(2)
	
	n.goto(0,0)
	n.write("OneTwoThreeFourFiveSix\n")
	n.write("Seven")
	
	n.set_char_brightness(8)
	n.write("Eight")
	n.set_char_brightness(2)
	
	n.write("NineTen\n")
	n.write("ElevenTwelveTwenty\n")
	n.write("ThirtyFourty")
	
	n.set_char_brightness(8)
	n.write("Fifty")
	n.set_char_brightness(2)
	
	n.write("OneTwo\n")
	n.write("ThreeFourFiveSix")
	
	n.set_char_brightness(8)
	n.write("Seven\n")
	n.set_char_brightness(2)
	
	n.write("EightNineAM")
	n.set_char_brightness(8)
	n.write("PM")
	
	#time.sleep(0.05)
	
	#n.write(sys.version+"\n")
	#n.write(repr(datetime.datetime.now()))
	#n.goto(1,1)
	#n.write("hi")