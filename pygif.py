from images2gif import writeGif
from PIL import Image, ImageSequence
import sys 
import os

from os import listdir
from os.path import isfile, join


def main(openfolder,savefolder,filename,sizex,sizey):
	seq=[]
	size = sizex, sizey
	#kwarg[1] should be the folder of the sequence
	onlyfiles = [ f for f in listdir(openfolder) if isfile(join(openfolder,f)) ]
	for img in onlyfiles:
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