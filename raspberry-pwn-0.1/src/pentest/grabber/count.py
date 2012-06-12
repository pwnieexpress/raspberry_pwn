# return the loc of the files
import os, sys, re


count = 0
python = re.compile(r'(.*).py$')
all = [f for f in os.listdir('./') if os.path.isfile(os.path.join('./', f)) and python.match(f)]
for a in all:
	print a
	try:
		f = open(a, 'r')
		for l in f.readlines():
			if len(l) > 0:
				count += 1
		f.close()
	except IOError:
		print "Prout!"

print "Lines of codes ", count


