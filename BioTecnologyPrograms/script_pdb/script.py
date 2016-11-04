# Author : Ronald Davi Rodrigues Pereira
# UFMG - Universidade Federal de Minas Gerais
# LBS - Laboratorio de Bioinformatica e Sistemas (Bioinformatics and systems laboratory)
# 
# License:
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Description:
# Python script to download .pdb files from rcsb.org and
# calculate possible covalent bond between protein atoms and binders
# 
# Running the script:
# python script.py -i "list of PDB names" -o "directory to download and to save others files" -d "cutoff distance"
# 
# -*- coding: utf-8 -*-

import urllib #importation to make the url download possible
import sys, getopt, os.path, os

lista_shr = 'hi:o:d:'
lista_ext = ["help","input-file","output-path","cutoff-distance"]

opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

try:
   opts , args = getopt.getopt(sys.argv[1:],lista_shr,lista_ext)

except getopt.GetoptError:
   print 'ERROR'
   sys.exit(1)

outputpath = ''
inputfile = ''
cutoff = 2

for opt, arg in opts:

	if opt ==  '-h' or opt == '--help':
		print 'test.py -i <input-file> -d <cutoff-distance> -o <output-path>'
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

# End of parameters passage

list_pdb = open(inputfile, 'r') # file with a list of proteins names to download

for line in list_pdb:
	line = line.strip('\n')
	pdb = line

	while os.path.exists(outputpath+'/%s.pdb'%pdb):
		line = list_pdb.next().strip('\n')
		pdb = line

# End of existance check of some PDB file

	print 'Downloading %s file......'%pdb
	
	f = open(outputpath+'/%s.pdb'%pdb,'w')
	f.write(urllib.urlopen('http://www.rcsb.org/pdb/files/'+pdb+'.pdb').read())
	f.close()
	# End of pdb file download

	file = open(outputpath+'/%s.pdb'%pdb, 'r')
	output = open(outputpath+'/%s_infos.pdb'%pdb, 'w')

	x = file.readlines()
	print 'Removing unnecessary informations......'

	for line in x:
		if line.startswith('ATOM') or line.startswith('HETATM'):
			output.write(line)

	file.close()
	output.close()

	# End of removal of unnecessary informations from the pdb file

	file = open(outputpath+'/%s_infos.pdb'%pdb, 'r')
	prot_atoms = open(outputpath+'/%s_atoms.pdb'%pdb, 'w')
	lig_atoms = open(outputpath+'/%s_heteroatoms.pdb'%pdb, 'w')

	x = file.readlines()
	print 'Separating atoms......'

	for line in x:
		if line.startswith('ATOM'):
			prot_atoms.write(line)
		else:
			lig_atoms.write(line)

	file.close()
	prot_atoms.close()
	lig_atoms.close()

	# End of separation of protein atoms in an file and atoms of the binders (heteroatoms) in another file

	file = open(outputpath+'/%s_infos.pdb'%pdb, 'r')
	output = open(outputpath+'/%s_possible_covalent.pdb'%pdb, 'w')
	print 'Calculating possible covalent bonds......'

	content = file.readlines()


	for line1 in content:
		if line1.startswith('ATOM'):
			x = float(line1[30:38]) # until position 37
			y = float(line1[38:46])
			z = float(line1[46:54])
			for line2 in content:
				if line2.startswith('HETATM'):
					a = float(line2[30:38])
					b = float(line2[38:46])
					c = float(line2[46:54])
					distance = ((((x-a)**2) + ((y-b)**2) + ((z-c)**2))**0.5)
					if distance < cutoff:
						atom_name = line1[12:16]
						residue_name = line1[17:20]
						residue_number = line1[22:26]
						residue_chain = line1[21]
						hetatm_name = line2[12:16]
						residue2_name = line2[17:20]
						residue2_number = line2[22:26]
						residue2_chain = line2[21]
						output.write(atom_name+' ; '+residue_name+' ; '+residue_number+' ; '+residue_chain+' ; '+str(distance)+' ; '+hetatm_name+' ; '+residue2_name+' ; '+residue2_number+' ; '+residue2_chain+'\n')
	file.close()
	output.close()
	# End of calculation of the distances between each atom and their possible existing covalent bonds (< 2 Angstroms) - (Sobolev)
list_pdb.close()
print 'Ready!'
# End of script
