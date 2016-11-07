# -*- coding: utf-8 -*-

import urllib #importation to make the url download possible
import sys, getopt, os.path, os

lista_shr = 'hi:o:d:'
lista_ext = ["help","input-file","output-path","cutoff-distance"]

opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

try:
   opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

except getopt.GetoptError:
   print 'ERROR\n'
   sys.exit(1)

outputpath = ''
inputfile = ''
cutoff = 2

for opt, arg in opts:

	if opt ==  '-h' or opt == '--help':
		print 'test.py -i <input-file> -o <output-path>'
		sys.exit()

	elif opt in ("-i", "--input-file"):
		inputfile = arg

	elif opt in ("-o", "--output-path"):
		outputpath = arg

	elif opt in ("-d", "--cutoff-distance"):
		cutoff = float(arg)

if os.path.exists(inputfile) == False:
	print 'Input file %s doesnt exist. Please check if the input file is in the same directory than the script.'%inputfile
	exit(1)

if os.path.exists(outputpath):
	print 'Output path (%s) already exists, but the file is saved anyway'%outputpath

if os.path.exists(outputpath) == False:
	os.mkdir(outputpath, 0755)
	print 'Directory created with sucess!'

inputfile = open(inputfile, 'r')

for line in inputfile:
	line = line.strip('\n')
	pdb = line

	pdbfile = open('%s.pdb'%pdb, 'r')
	out = open(outputpath+'/%s_model.pdb'%pdb, 'w')

	for line in pdbfile:
		line = line.strip('\n')
		pdbmodel = line
		if line.startswith('MODEL        1'):
			while line.startswith('ENDMDL') == False:
				line = pdbfile.next().strip('\n')
				pdbmodel = line
				if line.startswith('ANISOU') == False:
					out.write(line+'\n')

	pdbfile.close()
	out.close()
	# Considering only the first model and excluding the Anisotropic atoms


	f = open(outputpath+'/%s_model.pdb'%pdb, 'r')
	out = open(outputpath+'/%s_filter.pdb'%pdb, 'w')

	x = f.readlines()

	for line in x:
		if (line[17:20] == 'HOH' or line[77] == 'H') == False:
			out.write(line)

		# HOH and H filtering (excluding them from the PDB file)

	f.close()
	out.close()