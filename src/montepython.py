import speed_gen
import InputLoad
import CreateMol
import timeit
import direction_gen


st = timeit.default_timer()

inputs = InputLoad.LoadInputs()

#print (inputs.colRad)

for i in range (10000000):
    mol = CreateMol.Molecule(inputs,1,1)
#m, c = direction_gen.fit_line(0,0,1,1)

et = timeit.default_timer()

#print (m, c)
print (et - st)