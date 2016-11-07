# -*- coding: utf-8 -*-

import urllib #importation to make the url download possible
import sys, getopt, os.path, os

lista_shr = 'hi:o:n:'
lista_ext = ["help","input-file","output-path","binder-name"]

opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

try:
   opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

except getopt.GetoptError:
   print 'ERROR\n'
   sys.exit(1)

outputpath = ''
inputfile = ''
bindername = ''

for opt, arg in opts:

	if opt ==  '-h' or opt == '--help':
		print 'test.py -i <input-file> -n <binder-name(nome do ligante)> -o <output-path>'
		sys.exit()

	elif opt in ("-i", "--input-file"):
		inputfile = arg

	elif opt in ("-o", "--output-path"):
		outputpath = arg

	elif opt in ("-n", "--binder-name"):
		bindername = arg

if os.path.exists(inputfile) == False:
	print 'Input file %s doesnt exist. Please check if the input file is in the same directory than the script.'%inputfile
	exit(1)

if os.path.exists(outputpath):
	print 'Output path (%s) already exists, but the file is saved anyway'%outputpath

if os.path.exists(outputpath) == False:
	os.mkdir(outputpath, 0755)
	print 'Directory created with sucess!'

inputfile = open(inputfile,'r')

for line in inputfile:

	#Terminar de fazer o código de conversão de PDB para Mol2