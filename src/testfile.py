import speed_gen
import numpy

mean = numpy.array([1, 2])
sigma = numpy.array([1, 2])
weight = numpy.array([1, 2])

speed_gen.multi_gauss_speed(mean, sigma, weight)