import random
import math
import scipy.constants

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
# "Appropriated" from numerical recipes
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