from images2gif import writeGif
from PIL import Image, ImageSequence
import sys 
import os
import math

from os import listdir
from os.path import isfile, join

import subprocess

#i need to consider exr files
#just use rvio to deal with those
#https://docs.python.org/2/library/subprocess.html
#rvio file.*.exr -o file.#.jpg

#this also expects file to be name.frame.ext ie image.1.png
def reorder(a):
	# this is for re ordering sequences
	# we expect them to the number to be before the extensione, like so
	#file.whatever.num.ext
	ordered=range(len(a))
	for s in a:
		spl = s.split(".")
		ordered[ int(spl[len(spl)-2] )-1 ]=s
	return ordered

def gif_from_sequence(s,openfolder,savefolder,filename,sizex,sizey,time):
	seq=[]
	size = sizex, sizey
	for img in s:
		try:
			im = Image.open(openfolder+"/"+img)
			im.thumbnail(size, Image.ANTIALIAS)
			seq.append(im)
		except IOError:
			print "cannot resize for '%s'" % img

	#now lest try and make a gif
	writeGif(savefolder+"/"+filename+".gif", seq, duration=time, dither=0)
	print "made gif:"+filename

def main(openfolder,savefolder,filename,sizex,sizey,fps=24.0,max_frames=72):
	seqname=[]
	seqlength=[]
	seq=[]

	onlyfiles = [ f for f in listdir(openfolder) if isfile(join(openfolder,f)) ]

	for img in onlyfiles:
		spl = img.split(".")
		#ignore gifs that might be in there, because they are likely what we generate
		if spl[len(spl)-1] != "gif":
			if not spl[0] in seqname:
				#we have found a new seqence, add to the seq list
				seqname.append(spl[0])
				seqlength.append(1)
				group=[img,]
				seq.append(group)
			else:
				ind = seqname.index(spl[0])
				seqlength[ind] = seqlength[ind]+1
				seq[ind].append(img)

	#now i have my sequences grouped, sort them, and make the gif
	# i should also remove the frames that we dont needs as well here
	for s in seq:
		converted = False
		nspl = s[0].split(".")
		#first take care of conversion
		if nspl[len(nspl)-1] == "exr":
			#convert the sequence
			nspl[len(nspl)-2] = "@"
			o = ".".join(nspl)
			nspl[len(nspl)-2] = "#"
			nspl[len(nspl)-1] = "jpg"
			n = openfolder+"/"+".".join(nspl)
			f = openfolder+"/"+o
			subprocess.call(["rvio",f,"-o",n])
			#subprocess.Popen(["rvio",f,"-o",n])
			#p.wait()
			#now I need to rename the list to the newly converted file names
			for old in s:
				ospl = old.split(".")
				ospl[len(ospl)-1]="jpg"
				ospl[len(ospl)-2]= ospl[len(ospl)-2].zfill(4)
				s[s.index(old)] = ".".join(ospl)
			converted = True
		#
		s = reorder(s)
		#modulo out the frames we dont need
		modded = []
		count=0
		
		mod = math.ceil(float(seqlength[ seqname.index(nspl[0]) ])/float(max_frames))
		for r in s:
			if count%mod ==0:
				modded.append(r)
			count=count+1

		gif_from_sequence(modded,openfolder,savefolder,nspl[0]+"_"+filename,int(sizex),int(sizey),mod/fps)

		#now if we converted files, we can remove them
		if converted:
			for cfile in s:
				os.remove(openfolder+"/"+cfile)
