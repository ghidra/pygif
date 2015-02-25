import sys
import pygif

def main(kwargs):
	pygif.main(kwargs[1],kwargs[2],kwargs[3],kwargs[4],kwargs[5])

if __name__ == "__main__":
	main(sys.argv)