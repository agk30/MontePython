import numpy
import math
import sys
import getopt
import os
from tkinter import Tk     # from Tkinter import Tk for earlier than Python 3.x
from tkinter.filedialog import askdirectory, askopenfilename

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
    surface_list = ["SQA","SQE","IB","PFPE","OA","Bkg","InstrumFunc"]
    transition_list = ["Q11","Q12","Q13","Q14","Q15"]

    junk = []

    for name in name_list:
        if name in surface_list:
            surface = name
        elif name.isnumeric():
            delay = name
        elif name in transition_list:
            transition = name
        else:
            junk.append(name)
    
    if 'surface' not in locals():
        surface = -1

    if 'delay' not in locals():
        delay = -1

    if 'transition' not in locals():
        transition = -1

    return surface, delay, transition

def simple_split(file_path, delimiter):

    file_path = file_path.split(".")
    stem = file_path[0]
    name_list = stem.split(delimiter)

    found_delay = False

    for name in name_list:
        if name.isnumeric():
            delay =  name
            found_delay = True
            
    if found_delay:
        return delay
    else:
        print ("No delay found in image file name, did you use the right delimiter?")
        sys.exit()

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

def sum_tofs_named(folder_path):

    surface_list = ["SQA","SQE","IB","PFPE","OA"]
    transition_list = ["Q11","Q12","Q13","Q14","Q15"]
    
    delay_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            part_list = file.split("ChC")
            for part in part_list:
                if part.isnumeric():
                    delay = part
                    if not delay in delay_list:
                        delay_list.append(delay)

    delay_list.sort()
 
    summed_images = numpy.zeros((677,630,5,5,len(delay_list)))

    for root, dirs, files in os.walk(folder_path):
        #print (root)
        for name in root.split():
            #print (name)
            surface, delay, transition = parse_file_name(name)

            if (surface != -1) and (transition != -1):
                surface_index = surface_list.index(surface)
                transition_index = transition_list.index(transition)

                for file in os.listdir(root):
                    image = read_image(root+"/"+file)
                    delay = simple_split(file, "ChC")
                    summed_images[:,:,surface_index,transition_index,delay_list.index(delay)] = summed_images[:,:,surface_index,transition_index,delay_list.index(delay)] + image

    return summed_images, delay_list

def sum_tofs(path_list, delimiter):

    num_tofs = len(path_list)
    delay_list = []

    for root, dirs, files in os.walk(path_list[0]):
        for file in files:
            part_list = file.split(delimiter)
            for part in part_list:
                if part.isnumeric():
                    delay = part
                    if not delay in delay_list:
                        delay_list.append(delay)
    
    delay_list.sort()

    summed_images = numpy.zeros((420,420,len(delay_list)))

    for i in range(num_tofs):
        for root, dirs, files in os.walk(path_list[i]):
            for file in files:
                delay = simple_split(file, delimiter)
                image = read_image(root+"/"+file)
                summed_images[:,:,delay_list.index(delay)] = summed_images[:,:,delay_list.index(delay)] + image

    return summed_images, delay_list

def get_input_folder():

    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw() 
    # show an "Open" dialog box and return the path to the selected file
    input_path = askdirectory() 
    
    return input_path

def get_input_file():

    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw() 
    # show an "Open" dialog box and return the path to the selected file
    input_path = askopenfilename() 

    return input_path