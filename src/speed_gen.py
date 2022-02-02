import random
import math
import scipy.constants
import numpy

def ingoing_speed(x0,aMax, aMin, h, s, dist, pulseLength):

    # Calculate creation time, centred around t0, not beginning at t0
    t = random.random()
    t0 = (t*pulseLength) - (pulseLength/2)

    # Calculate TOF based on cumulative integral function from real data anf fit by Origin.
    # Function in Origin is called Logistics5.
    x = random.random()
    arrivalTime = x0/(((aMax-aMin)/(x-aMin))**(1/s)-1)**(1/h)
    speed = dist/(arrivalTime*1E-6)

    return t0, speed

def mb_prob(temp, speed, mass):

    # part 1, 2, 3 correspond to individual parts of the maxwell-boltzmann distribution
    # formula for calculating probability of a given speed
    part1 = 4*math.pi*speed*speed
    part2 = (mass/(2*math.pi*scipy.constants.Boltzmann*temp))**(3/2)
    part3 = math.exp((-mass*speed*speed)/(2*scipy.constants.Boltzmann*temp))

    probability = part1*part2*part3

    return probability

def mb_most_likely_prob(temp, mass):

    mostProbableSpeed = math.sqrt((2*scipy.constants.Boltzmann*temp)/mass)
    mostLikelyProbability = mb_prob(temp, mostProbableSpeed, mass)

    return mostLikelyProbability

def mb_speed(maxSpeed, temp, mass):

    mlp = mb_most_likely_prob(temp, mass)

    hit = False
    while not hit:
        rand1 = random.random()
        scatteredSpeed = maxSpeed*rand1

        probability = mb_prob(temp, scatteredSpeed, mass)

        # Calculates the probability of the speed with respect to the most probable speed equalling 1.
        # The Maxwell-Boltzmann distribution is already normalised to 1, meaning that the sum of all
        # probabilities from zero to infinity will equal 1.
        # It is possible to avoid this step, however, it would take a very long time to
        # achieve a hit due to the small value of probability.
        norm_probability = probability/mlp

        rand2 = random.random()

        if norm_probability > rand2:
            hit = True

    return scatteredSpeed

def lorentzian_distribution(gamma):

    rand = random.random()

    speed = gamma*math.tan(math.pi*(rand-0.5))

    return speed

# This method apparently is very efficient, however it generates two Gaussian distributed numbers at a time
# Make sure this is incorporated somehow to avoid wasting cycles
def gaussian_dsitribution(mean, sigma):

    hit = False
    while not hit:
        rand1 = random.random()
        rand2 = random.random()

        v1 = (2*rand1) - 1
        v2 = (2*rand2) - 1

        rSquared = (v1**2) + (v2**2)

        if rSquared < 1:
            z1 = v1*math.sqrt((-2*math.log(rSquared))/rSquared)
            z2 = v2*math.sqrt((-2*math.log(rSquared))/rSquared)

            z1 = mean + sigma*z1
            z2 = mean + sigma*z2

            hit = True

    return z1, z2

def transverse_speed(mean, sigma, gamma, l_g_fraction, zPos, travelDistance, startTime, speed, startPoint, vector):

    startTime = (startTime + abs(travelDistance/(vector[2]*speed)))
    startPoint[0] = startPoint[0] + (startTime*speed*vector[0])
    startPoint[1] = startPoint[1] + (startTime*speed*vector[1])
    startPoint[2] = zPos

    vector = vector*speed

    rand = random.random()

    if rand > l_g_fraction:
        transSpeed = lorentzian_distribution(gamma)
    else:
        transSpeed = gaussian_dsitribution(mean, sigma)

    vector[0] = transSpeed

    if rand > l_g_fraction:
        transSpeed = lorentzian_distribution(gamma)
    else:
        transSpeed = gaussian_dsitribution(mean, sigma)

    vector[1] = transSpeed

    vector = vector/numpy.linalg.norm(vector)

    return vector

def random_speed(low, high):

    rand = random.random()
    speed = ((high-low)*rand) + low

    return speed

def soft_sphere_speed(mass, internal_loss_ratio, surface_mass, initial_speed, deflection_angle):

    pi = scipy.constants.pi

    mass_ratio = mass/surface_mass*1000
    initial_energy = 0.5*mass*initial_speed*initial_speed
    deflection_angle = deflection_angle*((2*pi)/360)

    part1 = (2*mass_ratio)/((1+mass_ratio)**2)

    part2 = 1 + (mass_ratio*(math.sin(deflection_angle)**2))

    part3 = math.cos(deflection_angle)

    part4 = math.sqrt(1 - (mass_ratio*mass_ratio(math.sin(deflection_angle)**2)) - internal_loss_ratio*(mass_ratio + 1))

    part5 = internal_loss_ratio*((mass_ratio + 1)/(2*mass_ratio))

    energy_diff = part1*(part2 - (part3*part4) + part5)*initial_energy

    final_energy = initial_energy - energy_diff

    final_speed = math.sqrt(2*final_energy/mass)

    return final_speed

def multi_gauss_speed(gauss_mean_array, gauss_sigma_array, gauss_weight_array, dist, time_offset):

    m_size = len(gauss_mean_array)
    s_size = len(gauss_sigma_array)
    w_size = len(gauss_weight_array)

    # Checks that all parameter arrays are the same size
    if (m_size != s_size) or (m_size != w_size):
        print ("Error: Gauss parameter arrays must contain the same number of elements in each array")
    
    # Number of gaussians inferred from size of arrays. This can screw up if the arrays are not one dimensional, check this later.
    n_gaussians = m_size

    rand = random.random()

    # Arrival time is chosen from probability of the sum of the gaussians chosen. If random number is not chosen from the range of 0 to limit of first weighting,
    # it is then tries the range of the first weighting to the second weighting, then from the second to third if it is not successful etc. Weighting must sum to
    # unity for this to work.
    w_upper = 0
    w_lower = 0
    for i in range(n_gaussians):
        w_upper = w_upper + gauss_weight_array[i]

        if (rand > w_lower) and (rand < w_upper):
            arrival_time = numpy.random.normal(gauss_mean_array[i], gauss_sigma_array[i])
        
        w_lower =  w_lower + gauss_weight_array[i]

    arrival_time = arrival_time - time_offset
    speed = dist/(arrival_time*1E-6)

    return speed

def time_of_creation(pulse_length):

    rand = random.random()
    t0 = (pulse_length*rand) - (pulse_length/2)

    return t0
