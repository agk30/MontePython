import roi
import numpy
import os
import sys
import shutil

folder_path = roi.get_args(sys.argv[1:])

probe_height = 0
centre_point = [294, 210]
num_arcs = 7
num_wedges = 12

xPx = 420
yPx = 420

max_radius = 130

startTime = 68
endTime = 178
timeStep = 2

output_directory = "Output Data"

if not os.path.isdir(output_directory):
    os.mkdir(output_directory)
else:
    shutil.rmtree(output_directory)
    os.mkdir(output_directory)

num_timepoints = int((endTime - startTime) / timeStep) + 1
half_wedge_step = 90/num_wedges
half_arc_step = (max_radius/num_arcs)/2

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((num_arcs,num_wedges,int((endTime-startTime)/timeStep)+1,2))

radius = roi.generate_radii(num_arcs, max_radius)
wedge = roi.generate_wedges(num_wedges)
"""
for i in range(num_arcs):
    for j in range(num_wedges):
        if not os.path.isdir(output_directory+'/'+'/wedge '+str(round(wedge[j]-90-half_wedge_step,2))):
            os.mkdir(output_directory+'/'+'wedge '+str(round(wedge[j]-90-half_wedge_step,2)))
"""
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

#hacky way of making sure only images that fit the correct timestep are sampled
previous_value = startTime - timeStep
# Loops over every file in folder
for root, dirs, files in os.walk(folder_path):
    for name in files:
        file_path = root + "/" + name
        #surface, delay, transition = parse_file_name(file_path)
        delay = int(roi.simple_split(file_path))
        if (int(delay) <= endTime) and (int(delay) >= startTime):
            if (int(delay) - previous_value) == timeStep:
                timepoint_list.append(delay)
                print ('Processing '+name,end='\r')
                # For each file, data are read into the image matrix
                image = roi.read_image(file_path)
                # image goes to be processed, assigning the pixel intensity to the correct ROI
                outputArray[:,:,int((int(delay)-startTime)/timeStep),1] = roi.roi_assign(xPx, yPx, centre_point, radius, wedge, num_arcs, num_wedges, image)
                previous_value = delay
comment = str(radius)

delay_list = numpy.zeros((num_timepoints,1))

for i in range(num_timepoints):
    delay_list[i] = (startTime + i*timeStep)*1E-6

for j in range(num_wedges):
    with open(output_directory+'/wedge '+str(round(wedge[j]-90-half_wedge_step,2))+'.csv','wb') as f:
        write_array = outputArray[:,j,:,1]
        write_array = numpy.swapaxes(write_array, 0, 1)
        normalised_array = write_array.copy()
        for i in range(num_arcs):
            max_value = max(write_array[:,i])
            normalised_array[:,i] = normalised_array[:,i]/max_value
        
        #print (delay_list)
        #print (write_array)
        write_array = numpy.hstack((delay_list,write_array))
        write_array = numpy.hstack((write_array,normalised_array))
        numpy.savetxt(f, write_array, fmt='%.5e', delimiter=',', header=comment)

"""
for i in range(num_arcs):
    for j in range(num_wedges):
        #for k in range(num_timepoints):
            with open(output_directory+'/wedge '+str(round(wedge[j]-90-half_wedge_step,2))+'/arc '+str(round(radius[i]-half_arc_step,2))+'.csv','wb') as f:
                comment = 'start='+str(startTime)+', end='+str(endTime)+', radii='+str(radius)+', angles='+str(wedge)
                numpy.savetxt(f, outputArray[i,j,:,1], fmt='%.5e', delimiter=',')
"""

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

with open(output_directory+'/parameters.txt','wb') as f:
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