import inout
import molecule

inputs = inout.load_inputs()

floats_list = []

for item in inputs['math parameters']['gaussMeans'].split():
    floats_list.append(float(item))

inputs['math parameters']['gaussMeans'] = floats_list

#mol = molecule.Molecule(1, 1, inputs)