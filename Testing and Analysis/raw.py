import roi
import numpy
import os
import sys

folder_path = roi.get_args(sys.argv[1:])

probe_height = 0
centre_point = [294, 210]
num_arcs = 14
num_wedges = 14

xPx = 420
yPx = 420

max_radius = 158

startTime = 100
endTime = 200
timeStep = 1

if not os.path.isdir('Output Images'):
    os.mkdir('Output Images')

for i in range(num_arcs):
    for j in range(num_wedges):
        if not os.path.isdir('Output Images/'+'/wedge '+str(j+1)):
            os.mkdir('Output Images/'+'wedge '+str(j+1))

num_timepoints = int((endTime - startTime) / timeStep)

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((num_arcs,num_wedges,endTime-startTime+1,2))

radius = roi.generate_radii(num_arcs, max_radius)
wedge = roi.generate_wedges(num_wedges)

list = os.listdir(folder_path)
s_out_list = []
number_files = len(list)
print ('Total number of files = '+str(number_files)+', starting from '+str(startTime)+', ending at '+str(endTime))
# compiles list of surface out measurements
for file in list:
    for part in file.split("_"):
        if part == "IB":
            s_out_list.append(file)

timepoint_list = []

# Loops over every file in folder
for root, dirs, files in os.walk(folder_path):
    for name in files:
        file_path = root + "/" + name
        #surface, delay, transition = parse_file_name(file_path)
        delay = roi.simple_split(file_path)
        if (int(delay) <= endTime) and (int(delay) >= startTime):
            timepoint_list.append(delay)
            print ('Processing '+name,end='\r')
            # For each file, data are read into the image matrix
            image = roi.read_image(file_path)
            # image goes to be processed, assigning the pixel intensity to the correct ROI
            outputArray[:,:,int(delay)-startTime,1] = roi.roi_assign(xPx, yPx, centre_point, radius, wedge, num_arcs, num_wedges, image)

for i in range(num_arcs):
    for j in range(num_wedges):
        #for k in range(num_timepoints):
            with open('Output Images/'+'wedge '+str(j+1)+'/arc '+str(i+1)+'.csv','wb') as f:
                comment = 'start='+str(startTime)+', end='+str(endTime)+', radii='+str(radius)+', angles='+str(wedge)
                numpy.savetxt(f, outputArray[i,j,:,1], fmt='%.5e', delimiter=',')

#parameter_array = numpy.zeros((num_wedges,2))
#parameter_array[:,0] = wedge
#parameter_array[:,1] = radius

wedge = numpy.array(wedge)
radius = numpy.array(radius)

if num_arcs != num_wedges:
    if num_arcs > num_wedges:
        wedge = numpy.pad(wedge, (0,num_arcs-num_wedges))
        largest = num_arcs
    else:
        radius = numpy.pad(radius, (0,num_wedges-num_arcs))
        largest = num_wedges
else:
    largest = num_arcs

array = numpy.zeros((largest,2))
array[:,0] = radius
array[:,1] = wedge

with open('Output Images/parameters.txt','wb') as f:
    header_str = 'start time = '+str(startTime)+', end time = '+str(endTime)+', num radii = '+str(num_arcs)+', num angles = '+str(num_wedges)
    numpy.savetxt(f, array , fmt='%s', delimiter=',',header=header_str)
print ('')
print ('Done',end='\r')
print ('')

"""
selected_wedge = 0
sample_range_start = 0
sample_range_end = 5

sin = []
sout = []

fit = scipy.optimize.least_squares(residuals, 1)

modifier = fit.x

mod_sin = (sin*modifier) - sout
"""