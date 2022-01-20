import configparser

def load_inputs():
    
    config = configparser.ConfigParser()

    config.read("../inputs.cfg")

    return config