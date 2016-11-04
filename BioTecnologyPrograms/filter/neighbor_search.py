#!/usr/bin/python2.7
import sys

from Bio.PDB import PDBParser
from Bio.PDB import NeighborSearch
from Bio.PDB import Select, PDBIO

pdb_list = 'correct_cdk2_list'

pdb_path = 'CDK2_com_EDO/pdbs'
output_path = 'CDK2_com_EDO/pdb_atoms_filtered'

search_radius = 10

# PDBIO superscript in order to keep the atom number like in the original PDB file 
class PDBIO(PDBIO):

  def save(self, file, select=Select(), write_end=0):
        """
        @param file: output file
        @type file: string or filehandle 

        @param select: selects which entities will be written.
        @type select: 
            select hould have the following methods:
                - accept_model(model)
                - accept_chain(chain)
                - accept_residue(residue)
                - accept_atom(atom)
            These methods should return 1 if the entity
            is to be written out, 0 otherwise.

            Typically select is a subclass of L{Select}.
        """
        get_atom_line=self._get_atom_line
        if isinstance(file, basestring):
            fp=open(file, "w")
            close_file=1
        else:
            # filehandle, I hope :-)
            fp=file
            close_file=0
        # multiple models?
        if len(self.structure)>1 or self.use_model_flag:
            model_flag=1
        else:
            model_flag=0
        for model in self.structure.get_list():
            if not select.accept_model(model):
                continue
            # necessary for ENDMDL 
            # do not write ENDMDL if no residues were written
            # for this model
            model_residues_written=0

            # COMMENTED: now i keep the atom number like in the original PDB file
            #atom_number=1

            if model_flag:
                fp.write("MODEL      %s\n" % model.serial_num)
            for chain in model.get_list():
                if not select.accept_chain(chain):
                    continue
                chain_id=chain.get_id()
                # necessary for TER 
                # do not write TER if no residues were written
                # for this chain
                chain_residues_written=0
                for residue in chain.get_unpacked_list():
                    if not select.accept_residue(residue):
                        continue
                    hetfield, resseq, icode=residue.get_id()
                    resname=residue.get_resname()  
                    segid=residue.get_segid()
                    for atom in residue.get_unpacked_list():
                        if select.accept_atom(atom):
                            chain_residues_written=1
                            model_residues_written=1

                            # ADDED: now it keeps the atom number like in the original PDB file
                            atom_number = atom.get_serial_number()                   

                            s=get_atom_line(atom, hetfield, segid, atom_number, resname,
                                resseq, icode, chain_id)
                            fp.write(s)

                            # COMMENTED: now it keeps the atom number like in the original PDB file
                            #atom_number=atom_number+1                           

                if chain_residues_written:
                    fp.write("TER\n")
            if model_flag and model_residues_written:
                fp.write("ENDMDL\n")
            if write_end:
                fp.write('END\n')
        if close_file:
            fp.close()

class ResSelect(Select):
  def __init__(self,res_list):    
    self.res_list = res_list

  def accept_residue(self, res):
    if ( res in self.res_list ):      
      return True
    else:
      return False

def filter_structure(pdb,chain,lig,lig_num):
  # pdb_input = pdb_path + "/" + pdb + ":" + chain + ":" + lig + ":" + lig_num + ".atoms.pdb"
  pdb_input = pdb_path + "/" + pdb + ".pdb"
  pdb_output = output_path + "/" + pdb + ":" + chain + ":" + lig + ":" + lig_num + ".atoms.pdb"
  
  structure = PDBParser(QUIET=1).get_structure(pdb, pdb_input)
  atoms_pairs = NeighborSearch( list( structure.get_atoms() ) ).search_all(search_radius)

  res_list = set()

  for atom_pair in atoms_pairs:
    res1 = atom_pair[0].parent
    res_chain1 = res1.parent.id
    res_name1 = res1.resname
    res_num1 =  str(res1.id[1])  
  
    res2 = atom_pair[1].parent
    res_chain2 = res2.parent.id
    res_name2 = res2.resname
    res_num2 = str(res2.id[1])

    if ( (res_chain1 == chain and res_name1 == lig and res_num1 == lig_num) or (res_chain2 == chain and res_name2 == lig and res_num2 == lig_num) ):    
      res_list.add(res1)
      res_list.add(res2)  

  io = PDBIO()
  io.set_structure(structure)
  io.save(pdb_output, ResSelect(res_list))

FileIN = open(pdb_list,'r')
lines = FileIN.readlines()

for line in lines:
  line = line.strip('\n')
  (pdb,chain,lig,lig_num) = line.split(':')
  
  filter_structure(pdb,chain,lig,lig_num)



# search_radius = 10

# pdb_id = '3R73'
# pdb_file = pdb_id + '.pdb'

# chain = 'A'
# ligand_name = 'X87'
# ligand_num = '920'

# structure = PDBParser(QUIET=1).get_structure(pdb_id, pdb_file)
# atoms_pairs = NeighborSearch( list( structure.get_atoms() ) ).search_all(search_radius)

# filtered_pdb = ()

# res_list = set()

# for atom_pair in atoms_pairs:
#   res1 = atom_pair[0].parent
#   res_chain1 = res1.parent.id
#   res_name1 = res1.resname
#   res_num1 =  str(res1.id[1])  
  
#   res2 = atom_pair[1].parent
#   res_chain2 = res2.parent.id
#   res_name2 = res2.resname
#   res_num2 = str(res2.id[1])

#   if ( (res_chain1 == chain and res_name1 == ligand_name and res_num1 == ligand_num) or (res_chain2 == chain and res_name2 == ligand_name and res_num2 == ligand_num) ):    
#     res_list.add(res1)
#     res_list.add(res2)  

# class ResSelect(Select):
#   def accept_residue(self, res):
#     if ( res in res_list ):
#       return True
#     else:
#       return False

# io = PDBIO()
# io.set_structure(structure)
# io.save('teste.pdb',ResSelect())

# pymol_sel = ''
# pymol_list = []
# for res in res_list:  
#   res_chain1 = res.parent.id
#   res_name1 = res.resname
#   res_num1 =  str(res.id[1])  
  
#   pymol_list.append(res_num1)

# pymol_sel = "select res " + " or res ".join(pymol_list)
# print pymol_sel

