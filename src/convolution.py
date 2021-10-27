import numpy

def construct_kernel(row, column, kSize, padMatrix):

    if (kSize % 2) == 0:
        print("Kernel size must be an odd integer")

        return

    # kernel is output as a 1D array in wraparound oder
    wrapKernel = numpy.zeros((kSize**2))

    for i in range(kSize):
        for j in range(kSize):
            wrapKernel[((i-1)*kSize)+j] = padMatrix[(row+i), (column+j)]

    return wrapKernel


def savgol_coef_array(kSize):

    # reads in coefficient matrix
    coef_file = open("C:/Users/adam/Documents/Code/MontePython/sg_matrices/2D/CC_027x027_003x003.dat", "r")

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

    coef_file.close()

    # create numpy matrices needed
    # full matrix has all points in kernel (n) but single symmetric array is needed with length of (n-1)/2,
    # then a reversed array of the same length is used to fill out the other half of the full array
    coef_matrix = numpy.zeros((len(coef_list[0])))
    full_coef_matrix = numpy.zeros((kSize**2))
    rev_matrix = numpy.zeros((len(coef_list[0])))

    # coef_list has multiple dimensions, only top row is needed as the rest are to do with calculating derivatives
    coef_matrix = coef_list[0]
    # matrix is flipped to allow the other half to be written over more easily
    rev_matrix = numpy.flip(coef_matrix)

    # full coef matrix is written, extending the data from the file over to all pixels used in the kernel
    for i in range(int(len(coef_matrix)*2)-1):
        if i < len(coef_matrix):
            full_coef_matrix[i] = coef_matrix[i]
        else:
            full_coef_matrix[i] = rev_matrix[i-(int(((kSize**2)-1)/2))]

    return full_coef_matrix

def multi_sav_gol(xPx, yPx, kSize, matrix_file, kernel):

    # easier to use nd sometimes, calculates once instead of twice! WOW
    nd = int((kSize-1)/2)

    # matrix is initiated along with the padded matrix containing zeros all around to acommodate the kernel at the edges
    matrix = numpy.zeros((xPx,yPx))
    padMatrix = numpy.zeros((xPx+kSize-1,yPx+kSize-1))

    # think of a better way to do this. I mean, it works but it doesn't feel right
    i = 0
    for line in matrix_file:
        li=line.strip()
        matrix_line = [float(i) for i in li.split("	")]
        matrix[i][0:] = (matrix_line)
        i = i+1

    # tidy up by closing matrix file
    matrix_file.close()

    # assign padded matrix points from original image
    for i in range(xPx):
        for j in range(yPx):
            padMatrix[i+nd][j+nd] = matrix[i][j]

    # generate savgol coef array only once, used for duration of process
    coef_array = savgol_coef_array(kSize)

    # convolute image array by generating a kernel around interrogated point, then finding dot product with convolution matrix.
    # this leaves the new convoluted point in the processed image
    for i in range(xPx):
        for j in range(yPx):
            interrogate_point = numpy.dot(kernel, coef_array)
            matrix[i][j] = interrogate_point

    return matrix