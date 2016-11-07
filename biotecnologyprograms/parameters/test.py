# -*- coding: utf-8 -*-

import sys, getopt, os.path, os

lista_shr = 'hc''i:p''o:d'
lista_ext = ["help","clusters","input-file","path","output-path","destination"]

opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

try:
   opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

except getopt.GetoptError:
   print 'ERROR\n'
   sys.exit(1)

outputpath = ''
inputfile = ''

for opt, arg in opts:

	if opt ==  '-h' or opt == '--help':
		print 'test.py -i <input-file> -o <output-path>'
		sys.exit()

	elif opt in ("-i", "--input-file"):
		inputfile = arg

	elif opt in ("-o", "--output-path"):
		outputpath = arg

print 'Input file is : '+ inputfile
print 'Output path is : '+ outputpath

if os.path.exists(inputfile) == False:
	print 'Input file %s doesnt exist. Please check if the input file is in the same directory than the script.'%inputfile
	exit(1)

if os.path.exists(outputpath):
	print 'Output path %s already exists, but the file is saved anyway'%outputpath

if os.path.exists(outputpath) == False:
	os.mkdir(outputpath, 0755)
	print 'Directory created with sucess!'

file = open(inputfile, "r")
# Todo: Verificar se o arquivo já é existente

output = open(outputpath+'/%s'%inputfile, "w")

for line in file:
	output.write(line)