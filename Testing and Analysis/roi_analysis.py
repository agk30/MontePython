import numpy
import math
import os
import scipy.optimize

def arc_wedge(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges, radius, wedge):
    # finds the arc in which the pixel lies
    for i in range(max_num_radii):
        if dist_from_centre < radius[i]:
            selected_arc = i
            # Arc found!

    # finds the wedge in which the pixel lies
    angle = math.acos(math.radians(centre_point[2]-column)/dist_from_centre)
    for j in range(max_num_wedges):
        if angle < wedge[j]:
            selected_wedge = j
            # Wedge found!

    return selected_arc, selected_wedge

def roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, outputArray):

    for row in range(xPx):
        for column in range(yPx):
            dist_from_centre = math.sqrt((row-centre_point[1])**2 + (column-centre_point[2])**2)
            # Pixel must lie within the largest semi-circle to be processed
            if dist_from_centre < radius[max_num_radii-1]:
                arc, wedge = arc_wedge(row, column, centre_point, max_num_radii, max_num_wedges, radius, wedge)
                outputArray[arc][wedge] = outputArray[arc][wedge] + image[row][column]

    return outputArray

# angles generated here are defined as the boundaries between wedges
def generate_wedges(max_num_wedges):

    angle = []
    angle_increment = 180/max_num_wedges

    # half angle allows for offset on even numbers of angles to allow the middle of a wedge to be centred at 0 degrees
    if max_num_wedges%2 == 0:
        angle_offset = angle_increment/2
    else:
        angle_offset = 0

    for i in range(max_num_wedges):
        angle[i] = (i*angle_increment) + angle_offset
    
    return angle

def generate_radii(max_num_radii, max_radius):

    radius = []
    radius_increment = max_radius/max_num_radii

    for i in range(max_num_radii):
        radius[i] = (i+1)*radius_increment

    return radius

def read_image(image_path):

    with open(image_path, "r") as f:
        i = 0
        image = []
        for line in f:
            li=line.strip()
            matrix_line = [float(i) for i in li.split("	")]
            image[i][0:] = (matrix_line)
            i = i+1

    return image

def parse_file_name(file_path):

    name_list = file_path.split("_")
    for name in name_list:
        if name == "SQA" or "SQE" or "IB" or "PFPE":
            surface = name
        elif name.isnumeric() == True:
            delay = name
        elif name == "Q11" or "Q12" or "Q13" or "Q14" or "Q15":
            transition = name
    
    if 'surface' not in locals():
        print ("No surface name found")
        return

    if 'delay' not in locals():
        print ("No delay found in image name")
        return

    if 'transition' not in locals():
        print ("No transition found in image name")
        return

    return surface, delay, transition

def residuals(x, sin, sout):

    resid = (sin*x) - sout

    return resid

probe_height = 0
centre_point = []
num_arcs = 0
num_wedges = 0

xPx = 0
yPx = 0

max_num_radii = 0
max_num_wedges = 0
max_radius = 0

startTime = 0
endTime = 0
timeStep = 0

num_timepoints = (endTime - startTime) / timeStep

folder_path = ""
timePoint = ""

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((max_num_radii,max_num_wedges,2))

radius = generate_radii(max_num_radii, max_radius)
wedge = generate_wedges(max_num_wedges)

list = os.listdir(folder_path)
s_out_list = []
number_files = len(list)
print (number_files)

# compiles list of surface out measurements
for file in list:
    for part in file.split("_"):
        if part == "IB":
            s_out_list.append(file)

# Loops over every file in folder
for root, dirs, files in os.walk(folder_path):
    for name in files:
        file_path = root + "/" + name
        print (name)
        # For each file, data are read into the image matrix
        image = read_image(file_path)
        # image goes to be processed, assigning the pixel intensity to the correct ROI
        outputArray[:][:][timePoint][1] = roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, outputArray)
        # with open('Output Images/'+'sv_'+name+'.txt','wb') as f:
            #    numpy.savetxt(f, matrix, fmt='%.5e')

# TOF generation and manipulation

selected_wedge = 0
sample_range_start = 0
sample_range_end = 5

sin = []
sout = []

fit = scipy.optimize.least_squares(residuals, 1)

modifier = fit.x

mod_sin = (sin*modifier) - sout