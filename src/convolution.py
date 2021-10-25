import numpy

def construct_kernel(row, column, kSize, padMatrix):

    if (kSize % 2) == 0:
        print("Kernel size must be an odd integer")

        return

    # BROKEN AF FIX IT PLS
    # kernel is output as a 1D array in wraparound oder
    wrapKernel = numpy.zeros((kSize**2))

    for i in range(kSize):
        for j in range(kSize):
            wrapKernel[((i-1)*kSize)+j] = padMatrix[(row+i), (column+j)]

    return wrapKernel


def savgol_coef_array(kSize):

    # nd is points on either side of interrogation point, nk is 
    nd = (kSize-1)/2
    nk = ((kSize**2) - 1)/2

    # reads in coefficient matrix
    coef_file = open("../sg_matrices/2D/CC_003x003_001x001.dat", "r")

    # for matrix file, if line starts with #, it is ignored and the coefficent data are read
    coef_list = []
    for line in coef_file:
        # remove whitespace at start of line
        li=line.strip()
        # ignores commented lines
        if not li.startswith("#"):
            # removes S or A at beginning since we only need first line
            li = li[1:].strip()
            # turns stirng into floats
            f_list = [float(i) for i in li.split("	")]
            coef_list.append(f_list)

    coef_file = open("../sg_matrices/2D/CC_005x005_003x003.dat", "r")

    # for matrix file, if line starts with #, it is ignored and the coefficent data are read
    coef_list = []
    for line in coef_file:
        # remove whitespace at start of line
        li=line.strip()
        # ignors commented lines
        if not li.startswith("#"):
            # removes S or A at beginning since we only need first line
            li = li[1:].strip()
            # turns stirng into floats
            f_list = [float(i) for i in li.split("	")]
            coef_list.append(f_list)

    # create numpy matrices needed
    # full matrix has all points in kernel (n) but single symmetric array is needed with length of (n-1)/2,
    # then a reversed array of the same length is used to fill out the other half of the full array
    coef_matrix = numpy.zeros((len(coef_list[0])))
    full_coef_matrix = numpy.zeros((kSize**2))
    rev_matrix = numpy.zeros((len(coef_list[0])))

    coef_matrix = coef_list[0]
    rev_matrix = numpy.flip(coef_matrix)

    for i in range(int(len(coef_matrix)*2)-1):
        if i < len(coef_matrix):
            full_coef_matrix[i] = coef_matrix[i]
        else:
            full_coef_matrix[i] = rev_matrix[i-(int(((kSize**2)-1)/2))]

    return full_coef_matrix

def multi_sav_gol(xPx, yPx, kSize):

    nd = int((kSize-1)/2)

    matrix_file = open("D:/Scattering Images/2021-10-21_112004/Blurred Images/Image_077.txt", "r")

    matrix = numpy.zeros((xPx,yPx))
    padMatrix = numpy.zeros((xPx+nd,yPx+nd))

    i = 0
    for line in matrix_file:
        li=line.strip()
        matrix_line = [float(i) for i in li.split("  ")]
        matrix[i,:] = (matrix_line)
        i = i+1

    for i in range(xPx):
        for j in range(yPx):
            padMatrix[i+nd,j+nd] = matrix[i,j]

    #kernel = numpy.zeros((kSize))
    coef_array = numpy.zeros((kSize))

    for i in range(xPx+nd):
        for j in range(yPx+nd):
            kernel = construct_kernel(i+nd, j+nd, kSize, padMatrix)
            coef_array = savgol_coef_array(kSize)
            #print (kernel)
            #print (coef_array)
            interrogate_point = numpy.dot(kernel, coef_array)
            matrix[i,j] = interrogate_point

    return matrix
xPx = int(420)
yPx = int(420)
kSize = int(5)

matrix = multi_sav_gol(xPx,yPx,kSize)