import numpy
import scipy.signal
import matplotlib.pyplot as plt

input_path = r"C:\Users\adam\Documents\OH_FSpec.dat"
min_peak_height = 0.0015

with open(input_path,'r') as file:

    array = numpy.loadtxt(file)
    array_shape = numpy.shape(array)
    spectrum = numpy.zeros((array_shape[0],2))
    spectrum[:,0] = array[:,0]
    spectrum[:,1] = -array[:,3]

    peaks, _ = scipy.signal.find_peaks(spectrum[:,1], min_peak_height)

    plt.plot(spectrum[:,0],spectrum[:,1])
    plt.plot(spectrum[peaks,0], spectrum[peaks,1], "x")

    for i, txt in enumerate(peaks):
        plt.annotate(spectrum[txt,0], (spectrum[peaks[i],0], spectrum[peaks[i],1]))
        print(spectrum[txt,0], spectrum[i,1])

    plt.show()