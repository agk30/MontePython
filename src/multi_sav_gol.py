def construct_kernel(row, column, kSize, padMatrix):

    if (kSize % 2) != 0:
        print("Kernel size must be an odd integer")

        return

    # nd = kernel size minus 1, divided by 2
    #nd = (kSize - 1)/2

    # kernel is output as a 1D array in wraparound oder
    wrapKernel = [[kSize,kSize]]

    for i in range(len(kSize)):
        for j in range(len(kSize)):
            wrapKernel[((i-1)*kSize)+j] = padMatrix[(row+i), (column+j)]

    return wrapKernel


