import roi
import numpy
import os
import sys

folder_path = roi.get_args(sys.argv[1:])
print (folder_path)

probe_height = 0
centre_point = [294, 210]
num_arcs = 7
num_wedges = 14

xPx = 420
yPx = 420

max_num_radii = 7
max_num_wedges = 14
max_radius = 158

startTime = 56
endTime = 160
timeStep = 1

num_timepoints = int((endTime - startTime) / timeStep)

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((max_num_radii,max_num_wedges,endTime-startTime+1,2))

radius = roi.generate_radii(max_num_radii, max_radius)
wedge = roi.generate_wedges(max_num_wedges)

list = os.listdir(folder_path)
s_out_list = []
number_files = len(list)
print (number_files)

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
            print (name)
            # For each file, data are read into the image matrix
            image = roi.read_image(file_path)
            # image goes to be processed, assigning the pixel intensity to the correct ROI
            outputArray[:,:,int(delay)-startTime,1] = roi.roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, image)

# TOF generation and manipulation
if not os.path.isdir('Output Images'):
    os.mkdir('Output Images')

for i in range(max_num_radii):
    for j in range(max_num_wedges):
        if not os.path.isdir('Output Images/'+'/wedge'+str(j+1)):
            os.mkdir('Output Images/'+'wedge'+str(j+1))

file_header = ','.join(str(wedge))

for i in range(max_num_radii):
    for j in range(max_num_wedges):
        #for k in range(num_timepoints):
            with open('Output Images/'+'wedge'+str(j+1)+'/'+str(i+1)+'.csv','wb') as f:
                numpy.savetxt(f, outputArray[i,j,:,1], fmt='%.5e', delimiter=',',header='start='+str(startTime)+', end='+str(endTime))

print (radius)

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