import numpy
import math
import os

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

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((max_num_radii,max_num_wedges,2))

def arc_roi(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges):
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

radius = generate_radii(max_num_radii, max_radius)
angle = generate_wedges(max_num_wedges)

list = os.listdir(folder_path)
number_files = len(list)
print (number_files)

# Loops over every file in folder
for root, dirs, files in os.walk(folder_path):
    for name in files:
        file_path = root + "/" + name
        print (name)
        # For each file, data are read into the image matrix
        with open(file_path, "r") as f:
            i = 0
            for line in f:
                li=line.strip()
                matrix_line = [float(i) for i in li.split("	")]
                image[i][0:] = (matrix_line)
                i = i+1
        # For every pixel in image, the segment it belongs in is found
        for row in range(xPx):
            for column in range(yPx):
                dist_from_centre = math.sqrt((row-centre_point[1])**2 + (column-centre_point[2])**2)
                # Pixel must lie within the largest semi-circle to be processed
                if dist_from_centre < radius[max_num_radii-1]:
                    arc, wedge = arc_roi(row, column, centre_point, max_num_radii, max_num_wedges)
                    outputArray[arc,wedge,1] = outputArray[arc,wedge,1] + image[row,column]

        # with open('Output Images/'+'sv_'+name+'.txt','wb') as f:
            #    numpy.savetxt(f, matrix, fmt='%.5e')


