import random
import math
import numpy

def disc_pick():

    #Random number for distance point is from centre of unit circle the value is square rooted so that the points alone
    #this line will result in an even distribution of point on the unit circle rather than at a higher density at the centre
    rand1 = random.random()
    rand1 = math.sqrt(rand1)

    #Random number called for the angle this point is on the circle. The number is then converted into an angle in radians.
    rand2 = random.random()
    rand2 = math.sqrt(rand2)

    x = rand1*math.cos(rand2)
    y = rand1*math.sin(rand2)

    return x, y

def fit_line(y2, x2, y1, x1):

    m = (y2-y1)/(x2-x1)
    c = y2 - (m*x2)

    return m, c

def unit_vector(mx, my):

    magnitude = math.sqrt(mx**2 + my**2 + 1)
    vector = [mx/magnitude, my/magnitude, -1/magnitude]

    return vector

    
def ingoing_vector(valveRad, valvePos, skimRad, skimPos, colRad, colPos):

    hit = False
    while not hit:

        # Finds random point on valve for molecule origin
        valve[0,1] = disc_pick()
        valve = valve*valveRad
        valve[2] = valvePos

        # Finds random point on skimmer for molecule to pass through
        skimmer[0,1] = disc_pick()
        skimmer = skimmer*skimRad
        skimmer[2] = skimPos

        # Gradeint and intercept of line between valve and skimmer (mx and cx for x plane, my and cy for y plane)
        mx, cx = fit_line(valve[0], valve[2], skimmer[0], skimmer[2])
        my, cy = fit_line(valve[1], valve[2], skimmer[1], skimmer[2])

        # Calculates position at collimator distance and decides if it passes through or not
        collimator = float(0,0,0)
        collimator[0] = mx*(valvePos - colPos) + cx
        collimator[1] = my*(valvePos - colPos) + cy
        collimator[2] = colPos

        z = math.sqrt(collimator[0]**2 + collimator[1]((2)))

        if z < colRad:
            vector = unit_vector(mx,my)
            hit = True

def rotation(oldVector, theta):

    cosTheta = math.cos(theta*((2/math.pi)/360))
    sinTheta = math.sin(theta*((2/math.pi)/360))

    # this matrix is for roation about the y axis only. Rotation about any other axis will require a different matrix
    rotMatrix = numpy.zeros((3,3))
    rotMatrix(0,0) = cosTheta
    rotMatrix(0,2) = sinTheta
    rotMatrix(1,1) = 1
    rotMatrix(2,0) = -sinTheta
    rotMatrix(2,2) = cosTheta

    newVector = numpy.mathmul(rotMatrix, oldVector)

    return newVector

def cosine_distribution(cosPower):

    rand1 = random.random()
    rand2 = random.random()

    phi = rand1*2*math.pi

    x = rand2**(1/(cosPower+1))

    theta = math.cos(x)

    vector = float(0,0,0)
    vector[0] = (math.sin(theta))*(math.cos(phi))
    vector[1] = (math.sin(theta))*(math.sin(phi))
    vector[2] = math.cos(theta)

    return vector