import speed_gen
import InputLoad
import CreateMol

inputs = InputLoad.LoadInputs()

#print (inputs.colRad)

mol = CreateMol.Molecule(inputs,1,1)

print (mol.direction.value)