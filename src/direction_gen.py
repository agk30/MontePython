import random
import math
import numpy
import scipy.constants

def ingoing_direction(valve_rad, valve_pos, skim_rad, skim_pos, col_rad, col_pos):

    valve = numpy.zeros(3)
    skimmer = numpy.zeros(3)
    collimator = numpy.zeros(3)
    
    hit = False

    while not hit:
        valve[1], valve[2] = disc_pick()
        valve = valve*valve_rad
        valve[3] = valve_pos

        skimmer[1], skimmer[2] = disc_pick()
        skimmer = skimmer*skim_rad
        skimmer[3] = skim_pos

        mx, cx = fit_line(valve[1], valve[3], skimmer[1], skimmer[3])
        my, cy = fit_line(valve[2], valve[3], skimmer[2], skimmer[3])

        collimator[1] = mx*(valve_pos - col_pos) + cx
        collimator[2] = my*(valve_pos - col_pos) + cy
        collimator[3] = col_pos

        z = math.sqrt(collimator[1]**2 + collimator[2]**2)

        if z < col_rad:
            ingoing_unit_vector = unit_vector(mx, my)
            hit = True

    return ingoing_unit_vector


def disc_pick():

    rand1 = random.random()
    rand1 = math.sqrt(rand1)

    rand2 = random.random()
    rand2 = 2*scipy.constants.pi*rand2

    x = rand1*math.cos(rand2)
    y = rand1*math.sin(rand2)

    return x, y

def fit_line(y1, y2, x1, x2):

    m = (y2-y1)/(x2-x1)
    c = y2 - (m*x2)

    return m, c

def unit_vector(mx, my):

    v = numpy.zeros(3)

    magnitude = math.sqrt(mx**2 + my**2 + 1)
    v[1] = mx/magnitude
    v[2] = my/magnitude
    v[3] = -1/magnitude

    return v

def cosine_distribution(cosine_power):

    scatter_direction = numpy.zeros(3)

    rand1 = random.random()
    rand2 = random.random()

    phi = rand1*2*scipy.constants.pi

    x = rand2**(1/(cos_power+1))

    theta = scipy.acos(x)

    scatter_direction[0] = scipy.sin(theta)*scipy.cos(phi)
    scatter_direction[1] = scipy.sin(theta)*scipy.sin(phi)
    scatter_direction[2] = scipy.cos(theta)

    return scatter_direction