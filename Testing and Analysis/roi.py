import numpy
import math
import sys
import getopt

def arc_wedge(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges, radius, wedge):
    # finds the arc in which the pixel lies
    for i in range(max_num_radii):
        if dist_from_centre < radius[i]:
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

    return selected_arc, selected_wedge

def roi_assign(xPx, yPx, centre_point, radius, wedge, max_num_radii, max_num_wedges, image):

    working_array = numpy.zeros((max_num_radii, max_num_wedges))
    spillover = 0

    for row in range(xPx):
        for column in range(yPx):
            dist_from_centre = math.sqrt((row-centre_point[0])**2 + (column-centre_point[1])**2)

            # Pixel must lie within the largest semi-circle to be processed
            if (dist_from_centre < radius[max_num_radii-1]) and (dist_from_centre != 0):
                selected_arc, selected_wedge = arc_wedge(dist_from_centre, column, centre_point, max_num_radii, max_num_wedges, radius, wedge)
                if selected_wedge == -1:
                    #spillover
                    spillover = spillover + image[row,column]
                else:
                    working_array[selected_arc,selected_wedge] = working_array[selected_arc,selected_wedge] + image[row,column]

    return working_array

# angles generated here are defined as the boundaries between wedges
def generate_wedges(max_num_wedges):

    angle = numpy.zeros(max_num_wedges)
    angle_increment = 180/max_num_wedges

    # half angle allows for offset on even numbers of angles to allow the middle of a wedge to be centred at 0 degrees
    if max_num_wedges%2 == 0:
        angle_offset = angle_increment/2
    else:
        angle_offset = 0

    for i in range(max_num_wedges):
        angle[i] = ((i*angle_increment) + angle_offset)
    
    return angle

def generate_radii(max_num_radii, max_radius):

    radius = numpy.zeros((max_num_radii))
    radius_increment = max_radius/max_num_radii

    for i in range(max_num_radii):
        radius[i] = ((i+1)*radius_increment)

    return radius

def read_image(image_path):

    with open(image_path, "r") as f:
        image = numpy.loadtxt(f)

    return image

def parse_file_name(file_path):

    name_list = file_path.split("_")
    surface_list = ["SQA","SQE","IB","PFPE"]
    transition_list = ["Q11","Q12","Q13","Q14","Q15"]

    for name in name_list:
        if name in surface_list:
            surface = name
        elif name.isnumeric():
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

def get_args(argv):

    if not argv:
        print ('Please provide path to folder containing images')
        print ('raw.py -i <inputfolderpath>')
        sys.exit()

    path = ''

    try:
        opts, args = getopt.getopt(argv,"hi:",["input="])
    except getopt.GetoptError:
        print ('raw.py -i <inputfolderpath>')
        sys.exit(2)
    for opt, arg, in opts:
        if opt == '-h':
            print ('raw.py -i <inputfolderpath>')
            sys.exit()
        elif opt in ("-i", "--input"):
            path = arg

    return path