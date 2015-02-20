from images2gif import writeGif
from PIL import Image, ImageSequence
import sys 
import os
import math

from os import listdir
from os.path import isfile, join

#i need to consider exr files
#just use rvio to deal with those
#https://docs.python.org/2/library/subprocess.html
#rvio file.*.exr -o file.#.jpg
#i should also not add in every file, for file size
#do the math for the time between frames

#this also expects file to be name.frame.ext ie image.1.png


def main(openfolder,savefolder,filename,sizex,sizey,fps=24.0,max_frames=72):
	seq=[]
	size = sizex, sizey
	#kwarg[1] should be the folder of the sequence
	onlyfiles = [ f for f in sorted(listdir(openfolder)) if isfile(join(openfolder,f)) ]
	found = len(onlyfiles)
	mod = math.ceil(float(found)/float(max_frames))
	for img in onlyfiles:
		#loop the found files to weed out any that I cant use
		#splitim = img.split(".")
		# we ignore gif, because we assume they were what we craeted already, wo renders gif sequences
		#also ignore images that are past our mod
		#if(splitim[len(splitim)-1]!="gif" and float(splitim[len(splitim)-2])%mod == 0 ):

		#lets make the smaller first just incase
		try:
			splitim = img.split(".")
			if(splitim[len(splitim)-1]!="gif"):
				im = Image.open(openfolder+"/"+img)
				im.thumbnail(size, Image.ANTIALIAS)
				seq.append(im)
		except IOError:
			print "cannot resize for '%s'" % img

	#now lest try and make a gif
	writeGif(savefolder+"/"+filename+".gif", seq, duration=0.1, dither=0)