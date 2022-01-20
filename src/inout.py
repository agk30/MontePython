import configparser

def load_inputs():
    
    config = configparser.ConfigParser()

    config.read("../inputs.cfg")

    return config

# ASSIGN THE INPUTS TO PROPER VALUES HERE, HOW DID YOU NOT THINK OF THIS BEFORE