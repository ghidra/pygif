Python script to make a gif from a sequence.
----

run:

python makegif.py [arguments]

Takes 5 arguments

-Folder to get sequence from
	-only works on files types that PIL supports
-Folder to save resulting gif to
-File name for resulting gif, without the extension
-maximum size in x
-maximum size in y

ie:

python makegif.py /seq /seq newgif 256 256