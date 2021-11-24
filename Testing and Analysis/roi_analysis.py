import numpy
import math
import os
import scipy.optimize
import sys

def arc_wedge(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges, radius, wedge):
    # finds the arc in which the pixel lies
    for i in range(max_num_radii):
        if dist_from_centre < radius[i]:
            #print ("here")
            selected_arc = i
            break

    # finds the wedge in which the pixel lies
    angle = math.degrees(math.acos((centre_point[1]-column)/dist_from_centre))
    for j in range(max_num_wedges):
        if angle < wedge[j]:
            selected_wedge = j
            break
        # if angle is beyond largest angle slice, needs to be collected in spillover
        else:
            selected_wedge = -1
        # Wedge found!
        #print (angle)

    return selected_arc, selected_wedge

def roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, image):

    working_array = numpy.zeros((max_num_radii, max_num_wedges))
    spillover = 0

    for row in range(xPx):
        for column in range(yPx):
            dist_from_centre = math.sqrt((row-centre_point[0])**2 + (column-centre_point[1])**2)

            #print (dist_from_centre, radius[max_num_radii-1])
            
            # Pixel must lie within the largest semi-circle to be processed
            if (dist_from_centre < radius[max_num_radii-1]) and (dist_from_centre != 0):
                
                #print (dist_from_centre, radius[max_num_radii-1])
                selected_arc, selected_wedge = arc_wedge(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges, radius, wedge)
                if selected_wedge == -1:
                    #spillover
                    spillover = spillover + image[row,column]
                else:
                    #print (selected_arc,selected_wedge,row,column)
                    working_array[selected_arc,selected_wedge] = working_array[selected_arc,selected_wedge] + image[row,column]

                #print (working_array[selected_arc][selected_wedge], selected_arc, selected_wedge)
    return working_array

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
        angle.append((i*angle_increment) + angle_offset)
        #angle[i] = (i*angle_increment) + angle_offset
    
    return angle

def generate_radii(max_num_radii, max_radius):

    radius = []
    radius_increment = max_radius/max_num_radii

    for i in range(max_num_radii):
        radius.append((i+1)*radius_increment)
        #radius[i] = (i+1)*radius_increment
    
    print (radius)

    return radius

def read_image(image_path):

    illegal_characters = ['','\n']

    with open(image_path, "r") as f:
        i = 0

        image = numpy.loadtxt(f)
        #print (image)

        #image = [[float(num) for num in line.split('  ')] for line in f]

        """
        working_line = []
        for line in f:
            #li=line.strip()
            num = line.split(" ")
            for element in num:
                element = element.strip()
                if element not in illegal_characters:
                    working_line.append(element)
            #matrix_line = [float(i) for i in li.split(" ")]
            matrix_line = [float(i) for i in working_line]
            print (len(matrix_line))
            #image[i,:] = (matrix_line)
            #image.append(matrix_line)
            i = i+1
            """

    return image

def parse_file_name(file_path):

    name_list = file_path.split("_")
    surface_list = ["SQA","SQE","IB","PFPE"]
    transition_list = ["Q11","Q12","Q13","Q14","Q15"]

    for name in name_list:
        if name in surface_list:
            surface = name
        elif name.isnumeric() == True:
            delay = name
        elif name in transition_list:
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

def simple_split(file_path):

    file_path = file_path.split(".")
    name_list = file_path[0].split("_")

    for name in name_list:

        if name.isnumeric():
            delay =  name
            return delay

def residuals(x, sin, sout):

    resid = (sin*x) - sout

    return resid

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

############################# IMPORTANT #################################
#matrix[:,:,0,0] = smaller_matrix
######################### END OF IMPORTANT ##############################

num_timepoints = int((endTime - startTime) / timeStep)

folder_path = "K:/Scattering Images/2021-11-24_152758/Blurred Images"
#timePoint = ""

image = numpy.zeros((xPx,yPx))
outputArray = numpy.zeros((max_num_radii,max_num_wedges,endTime-startTime+1,2))

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

timepoint_list = []

# Loops over every file in folder
for root, dirs, files in os.walk(folder_path):
    for name in files:
        file_path = root + "/" + name
        #surface, delay, transition = parse_file_name(file_path)
        delay = simple_split(file_path)
        if (int(delay) <= endTime) and (int(delay) >= startTime):
            timepoint_list.append(delay)
            print (name)
            # For each file, data are read into the image matrix
            image = read_image(file_path)
            # image goes to be processed, assigning the pixel intensity to the correct ROI
            outputArray[:,:,int(delay)-startTime,1] = roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, image)

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